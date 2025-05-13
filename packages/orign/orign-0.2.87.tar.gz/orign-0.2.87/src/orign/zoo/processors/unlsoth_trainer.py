import os
import random
import string
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from nebu import Message, Processor, processor
from nebu.config import GlobalConfig as NebuGlobalConfig
from nebu.containers.models import V1EnvVar
from nebu.processors.models import (
    V1Scale,
    V1ScaleDown,
    V1ScaleUp,
    V1ScaleZero,
)
from pydantic import BaseModel

from orign import V1TrainingStatus


class TrainingRequest(BaseModel):
    adapter: str
    dataset: str
    model: str = "unsloth/Qwen2.5-VL-32B-Instruct"
    max_length: int = 32_768
    epochs: int = 2
    batch_size: int = 2
    gradient_accumulation_steps: int = 4
    learning_rate: float = 2e-4
    weight_decay: float = 0.01
    warmup_steps: int = 5
    logging_steps: int = 1
    save_steps: int = 5
    lora_alpha: int = 128
    lora_rank: int = 64
    lora_dropout: float = 0
    optimizer: str = "adamw_8bit"
    owner: Optional[str] = None
    labels: Optional[Dict[str, str]] = None


class TrainingResponse(BaseModel):
    loss: float
    train_steps_per_second: float
    train_samples_per_second: float
    train_runtime: float
    adapter: str
    adapter_uri: str


scale = V1Scale(
    up=V1ScaleUp(above_pressure=10, duration="5m"),
    down=V1ScaleDown(below_pressure=2, duration="10m"),
    zero=V1ScaleZero(duration="10m"),
)

setup_script = """
apt update
apt install -y git
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pip install trl peft transformers bitsandbytes sentencepiece accelerate orign
pip uninstall -y xformers
pip install -U xformers --index-url https://download.pytorch.org/whl/cu126
pip install -e git+https://github.com/pbarker/unsloth-zoo.git#egg=unsloth_zoo
pip install unsloth
pip install -e git+https://github.com/pbarker/unsloth-zoo.git#egg=unsloth_zoo
pip install huggingface_hub[hf_xet]
"""
# pip install -e git+https://github.com/pbarker/unsloth.git#egg=unsloth


BASE_MODEL_ID = os.getenv("BASE_MODEL_ID", "unsloth/Qwen2.5-VL-32B-Instruct")


def init():
    import gc
    import os

    from unsloth import FastVisionModel  # type: ignore # isort: skip
    import torch  # type: ignore
    from nebu import Cache  # type: ignore

    if "state" in globals():  # <-- already loaded by an earlier worker
        print("state already loaded by an earlier worker")
        return

    gc.collect()
    torch.cuda.empty_cache()

    # os.environ.setdefault("MAX_PIXELS", "100352")

    @dataclass
    class InferenceState:
        base_model: (
            Any  # Changed from FastVisionModel for PeftModel compatibility below
        )
        model_processor: Any
        base_model_id: str
        cache: Cache

    print("loading model...")
    print("--- nvidia-smi before load ---")
    os.system("nvidia-smi")
    print("--- end nvidia-smi before load ---")
    time_start_load = time.time()
    base_model, model_processor = FastVisionModel.from_pretrained(
        BASE_MODEL_ID,
        load_in_4bit=False,
        # use_fast=True,
        dtype=torch.bfloat16,
        max_seq_length=32_768,
    )
    print(f"Loaded model in {time.time() - time_start_load} seconds")
    print("--- nvidia-smi after load ---")
    os.system("nvidia-smi")
    print("--- end nvidia-smi after load ---")

    global state
    state = InferenceState(
        base_model=base_model,
        model_processor=model_processor,
        base_model_id=BASE_MODEL_ID,
        cache=Cache(),
    )


def train_unsloth_sft(message: Message[TrainingRequest]) -> TrainingResponse:
    import json
    import time

    import requests

    # Import necessary PEFT components
    from peft import LoraConfig, PeftModel  # type: ignore
    from unsloth import FastVisionModel, is_bf16_supported  # type: ignore # isort: skip
    from unsloth.trainer import UnslothVisionDataCollator  # type: ignore # isort: skip

    # Perform a comprehensive state reset at the beginning of each message processing
    # This helps prevent issues with meta tensors between consecutive runs
    import gc

    import torch  # type: ignore
    from chatmux import oai_to_unsloth
    from nebu import (
        Bucket,
        ContainerConfig,
        V1ResourceReference,
        is_allowed,
    )
    from trl import SFTConfig, SFTTrainer  # type: ignore

    from orign import Adapter, Training, V1LoraParams

    # First ensure CUDA cache is cleared
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

    # Force garbage collection multiple times to ensure all tensors are released
    gc.collect()

    global state

    print("message", message)
    if not message.content:
        raise ValueError("No training request provided")
    training_request: TrainingRequest = message.content

    container_config = ContainerConfig.from_env()
    print("container_config", container_config)

    bucket = Bucket()

    print("loading model...")
    adapter_uri = (
        f"{container_config.namespace_volume_uri}/adapters/{training_request.adapter}"
    )
    time_start_load = time.time()
    # Initialize model_to_train which will hold the PEFT model
    model_to_train = None
    # tokenizer = None # Initialize tokenizer to None - Now fetched from state

    adapter_parts = training_request.adapter.split("/")
    if len(adapter_parts) == 2:
        adapter_namespace = adapter_parts[0]
        adapter_name = adapter_parts[1]
    else:
        adapter_name = training_request.adapter
        if training_request.owner:
            adapter_namespace = training_request.owner
        else:
            adapter_namespace = message.handle

    # Ensure adapter_namespace is set
    if not adapter_namespace:
        raise ValueError("Could not determine adapter namespace for training log")

    if training_request.labels:
        training_labels = training_request.labels.copy()
    else:
        training_labels = {}
    training_labels["message_id"] = message.id
    training_labels["container_id"] = os.getenv("NEBU_CONTAINER_ID", "unknown")
    random_chars = "".join(random.choices(string.ascii_letters + string.digits, k=5))

    adapter_ref = V1ResourceReference(
        name=adapter_name,
        namespace=adapter_namespace,
        kind="Adapter",
    )
    print("adapter_ref: ", adapter_ref)

    training = None
    adapter_name_for_peft = "default"  # Initialize here
    failure = False  # Initialize failure flag here
    try:
        print("creating training with api_key", message.api_key)
        config_data = message.model_dump()
        config_data.pop("api_key", None)

        training = Training(
            name=adapter_name + "-" + random_chars,
            namespace=adapter_namespace,
            config_data=config_data,
            adapter=adapter_ref,
            labels=training_labels,
            unique_adapter_active=True,
            api_key=message.api_key,
        )
        print("\n >> marking initial training as running")
        training.update(status=V1TrainingStatus.RUNNING)

        adapter = None
        epochs_trained = 0  # Initialize here
        checkpoint_path = None  # Initialize here
        try:
            adapters = Adapter.get(
                adapter_namespace, adapter_name, api_key=message.api_key
            )
        except Exception:
            adapters = []
        print("found adapters", adapters)

        if adapters:
            adapter = adapters[0]

        if adapter:
            print("Found adapter: ", adapter)

            epochs_trained = adapter.epochs_trained

            if not is_allowed(adapter.metadata.owner, message.user_id, message.orgs):
                raise ValueError("You are not allowed to train this existing adapter")

            # Store the local path where the adapter will be synced
            # Use a temporary, unique path for each run to avoid conflicts
            random_suffix = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=8)
            )
            local_adapter_path = f"/tmp/adapter_sync_{random_suffix}"
            os.makedirs(local_adapter_path, exist_ok=True)
            print(f"Local adapter path for sync: {local_adapter_path}")

            time_start = time.time()
            try:
                bucket.sync(adapter.uri, local_adapter_path)
                print(f"Synced in {time.time() - time_start} seconds")

                # Load the adapter onto the base model from state
                print(f"Loading adapter from {local_adapter_path} onto base model...")
                # Use PeftModel.from_pretrained to load adapter onto the base model
                model_to_train = PeftModel.from_pretrained(
                    state.base_model,
                    local_adapter_path,
                    is_trainable=True,
                    adapter_name=adapter_name_for_peft,
                )
                # The checkpoint path for the trainer is the directory containing adapter_model.safetensors etc.
                checkpoint_path = local_adapter_path
                print(f"Adapter '{adapter_name_for_peft}' loaded onto base model.")

                # Check if the loaded model has PEFT adapters active *after* successful load
                if hasattr(model_to_train, "print_trainable_parameters"):
                    model_to_train.print_trainable_parameters()
                else:
                    print(
                        "Model does not have PEFT structure or print_trainable_parameters method after loading adapter."
                    )

                # Apply Unsloth post-patching after loading existing adapter
                print("Applying Unsloth post-patch model...")
                model_to_train = FastVisionModel.post_patch_model(
                    model_to_train,
                    # use_gradient_checkpointing=True,  # Or based on a config flag if needed
                )
                print("Unsloth post-patch model applied after loading.")

            except Exception as e:
                print(
                    f"Error syncing or loading adapter from {local_adapter_path}: {e}"
                )
                print("Proceeding to train a new adapter instead.")
                checkpoint_path = None
                # Clean up failed sync directory
                if os.path.exists(local_adapter_path):
                    import shutil

                    shutil.rmtree(local_adapter_path)

        # If no existing adapter or loading failed, create a new one
        if not model_to_train:
            print(
                "Initializing NEW PEFT LoRA adapter on base model using FastVisionModel.get_peft_model..."
            )
            # Apply LoRA config to the base model from state using Unsloth's method
            model_to_train = FastVisionModel.get_peft_model(
                state.base_model,
                r=training_request.lora_rank,
                lora_alpha=training_request.lora_alpha,
                lora_dropout=training_request.lora_dropout,
                bias="none",
                # target_modules="all-linear",  # Let unsloth handle targeting based on flags if needed
                # Pass finetuning flags directly if supported by unsloth's get_peft_model
                finetune_vision_layers=True,
                finetune_language_layers=True,
                finetune_attention_modules=True,
                finetune_mlp_modules=True,
                # use_gradient_checkpointing=True,  # Ensure this is passed for setup
                random_state=3407,
                # max_seq_length=training_request.max_length, # Max seq length should be on base model
                use_rslora=False,
                # modules_to_save=None, # Add if needed
                init_lora_weights=True,  # Default True
                # loftq_config={}, # Add if needed
                adapter_name=adapter_name_for_peft,  # Assign a name
            )
            print(f"New LoRA adapter '{adapter_name_for_peft}' created.")
            epochs_trained = 0  # Reset epochs trained for new adapter
            checkpoint_path = None  # No checkpoint to resume from

            if hasattr(model_to_train, "print_trainable_parameters"):
                model_to_train.print_trainable_parameters()

        print(f"Adapter setup completed in {time.time() - time_start_load} seconds")

        # Removed model printing here as it can be very large

        print("Downloading dataset")
        time_start_download = time.time()
        response = requests.get(training_request.dataset)
        response.raise_for_status()  # optional: raises if request failed
        print(f"Downloaded dataset in {time.time() - time_start_download} seconds")

        # Decode and split into lines
        lines = response.content.decode("utf-8").splitlines()

        # Parse and convert each JSON line
        time_start_convert = time.time()
        converted_dataset = [
            oai_to_unsloth(json.loads(line)) for line in lines if line.strip()
        ]
        print(f"Converted dataset in {time.time() - time_start_convert} seconds")
        print("dataset example", converted_dataset[:1])

        # Enable training mode for the PEFT model
        # FastVisionModel.for_training(model) # Apply to the PEFT model
        if hasattr(model_to_train, "enable_input_require_grads"):
            model_to_train.enable_input_require_grads()  # Common PEFT practice

        train_epochs = epochs_trained + training_request.epochs
        print("training_request.epochs", training_request.epochs)
        print("epochs_trained", epochs_trained)
        print(f"train_epochs: {train_epochs}")

        # When continuing training, skip token embedding correction to avoid meta tensor issues
        # skip_token_correction = is_continue # Removed this logic, may not be needed with PEFT loading

        output_dir = "outputs"
        # Ensure output_dir is clean before training
        if os.path.exists(output_dir):
            import shutil

            shutil.rmtree(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        trainer = SFTTrainer(
            model=model_to_train,  # Use the PEFT model
            tokenizer=state.model_processor,  # Use tokenizer from state
            data_collator=UnslothVisionDataCollator(
                model_to_train, state.model_processor, resize="max"
            ),  # Use PEFT model here too
            train_dataset=converted_dataset,
            args=SFTConfig(
                per_device_train_batch_size=training_request.batch_size,
                gradient_accumulation_steps=training_request.gradient_accumulation_steps,
                warmup_steps=training_request.warmup_steps,
                # max_steps=training_request.max_steps,
                num_train_epochs=train_epochs,
                learning_rate=training_request.learning_rate,
                fp16=not is_bf16_supported(),
                bf16=is_bf16_supported(),
                logging_steps=training_request.logging_steps,
                optim=training_request.optimizer,
                weight_decay=training_request.weight_decay,
                lr_scheduler_type="linear",
                seed=3407,
                output_dir=output_dir,  # Use the variable defined above
                report_to="none",  # For Weights and Biases
                save_strategy="no",  # No automatic saving during training
                # gradient_checkpointing=True,  # Enable gradient checkpointing if needed
                # gradient_checkpointing_kwargs={
                #     "use_reentrant": False
                # },  # Recommended for newer torch
                # save_steps is not needed if save_strategy is "no"
                # You MUST put the below items for vision finetuning:
                remove_unused_columns=False,
                dataset_text_field="",  # Keep empty for vision
                # dataset_kwargs={ # Removed skip_token_correction
                #     "skip_prepare_dataset": True,
                # },
                dataset_kwargs={"skip_prepare_dataset": True},
                dataset_num_proc=4,
                max_seq_length=training_request.max_length,
            ),
        )

        # Set environment variable for Unsloth to return logits
        os.environ["UNSLOTH_RETURN_LOGITS"] = "1"

        time_start_train = time.time()
        try:
            print(
                f"Starting trainer.train(resume_from_checkpoint={checkpoint_path})..."
            )
            # Pass the path to the *adapter* checkpoint if resuming
            trainer_stats = trainer.train(
                resume_from_checkpoint=checkpoint_path  # Pass the determined checkpoint path
            )
            print(trainer_stats)

            # Explicitly save the final model, tokenizer, and trainer state
            print(f"Explicitly saving final model and state to {output_dir}...")
            trainer.save_model(output_dir)
            trainer.save_state()  # Saves trainer_state.json to output_dir
            print("Final model and state saved.")

        except NotImplementedError as e:
            if "Cannot copy out of meta tensor" in str(e):
                print(
                    "Meta tensor error encountered - this might occur when training the same adapter twice in succession"
                )
                print("Error details:", str(e))
                print("Try running the training in a new process or container")
                # Set a default value for trainer_stats
                trainer_stats = {"train_runtime": time.time() - time_start_train}
                # Still allow the function to complete and return some metrics
            else:
                # Re-raise if it's a different NotImplementedError
                raise
        print(f"Trained in {time.time() - time_start_train} seconds")

        # The HuggingFace Trainer saves the final model and state to `args.output_dir`.
        # So, `output_dir` ("outputs") itself should contain the final version.
        # With save_strategy="no", we've explicitly saved it above.
        final_model_directory = output_dir  # This is "outputs"

        print(f"Final model and state are expected in: {final_model_directory}")

        # Initialize metrics dict as empty
        training_metrics = {}

        # Check if output_dir (final_model_directory) exists
        if os.path.exists(final_model_directory):
            print(
                f"Copying contents of {final_model_directory} to bucket for adapter URI: {adapter_uri}"
            )
            bucket.copy(
                final_model_directory,
                adapter_uri,
            )
            # Try to load the trainer_state.json from this final directory
            trainer_state_path = os.path.join(
                final_model_directory, "trainer_state.json"
            )
            if os.path.exists(trainer_state_path):
                try:
                    with open(trainer_state_path, "r") as f:
                        state_data = json.load(f)
                    training_metrics = state_data  # Use the entire loaded state
                    print(f"Loaded full state from {trainer_state_path}")
                    if state_data:
                        print(
                            f"  Final trainer_state - epoch: {state_data.get('epoch')}"
                        )
                        print(
                            f"  Final trainer_state - global_step: {state_data.get('global_step')}"
                        )
                        # log_history is a list, show the last entry if it exists
                        log_history = state_data.get("log_history", [])
                        if log_history:
                            print(
                                f"  Final trainer_state - last log_history entry: {log_history[-1]}"
                            )
                except Exception as e:
                    print(
                        f"Warning: Failed to read/parse {trainer_state_path}: {e}. Proceeding without metrics from state file."
                    )
            else:
                print(
                    f"Warning: {trainer_state_path} not found in {final_model_directory}. Proceeding without metrics from state file."
                )
        else:
            print(
                f"Warning: Output directory {final_model_directory} not found. Cannot save model or metrics."
            )

        past_ex_trained = 0
        adapters = Adapter.get(adapter_namespace, adapter_name, api_key=message.api_key)
        if adapters:
            adapter = adapters[0]
            past_ex_trained = adapter.examples_trained

        adapter = Adapter(
            name=adapter_name,
            namespace=adapter_namespace,
            uri=adapter_uri,
            owner=message.content.owner if message.content.owner else message.user_id,  # type: ignore
            base_model=training_request.model,
            epochs_trained=train_epochs,
            examples_trained=past_ex_trained + len(converted_dataset),
            last_trained=int(time.time()),
            lora=V1LoraParams(
                r=training_request.lora_rank,
                alpha=training_request.lora_alpha,
                dropout=training_request.lora_dropout,
            ),
            labels=training_request.labels,
            api_key=message.api_key,
        )

        training.log(data=training_metrics)
        training.update(status=V1TrainingStatus.COMPLETED)

        # --- Unload Adapter ---
        print(f"Unloading adapter '{adapter_name_for_peft}' from the base model...")
        if model_to_train and hasattr(model_to_train, "unload"):
            try:
                # Ensure model is on CPU before unloading if necessary, or handle potential GPU memory issues
                # model_to_train.to('cpu') # Optional: move to CPU first if unload causes GPU issues
                model_to_train.unload()
                print(f"Adapter '{adapter_name_for_peft}' unloaded successfully.")
            except Exception as unload_e:
                print(
                    f"Warning: Failed to unload adapter '{adapter_name_for_peft}': {unload_e}"
                )
        else:
            print(
                f"Model object {type(model_to_train)} does not have 'unload' method or is None."
            )
        # ----------------------

        # Force cleanup after unloading
        model_to_train = None  # Clear reference
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
        print("Post-training cleanup finished.")

        return TrainingResponse(
            loss=training_metrics.get("loss", 0.0),
            train_steps_per_second=training_metrics.get("train_steps_per_second", 0.0),
            train_samples_per_second=training_metrics.get(
                "train_samples_per_second", 0.0
            ),
            train_runtime=training_metrics.get("train_runtime", 0.0),
            adapter=training_request.adapter,
            adapter_uri=adapter_uri,
        )
    except Exception as e:
        print(f"Error training unsloth: {e}")
        failure = True
        if training:
            print("\n >> marking final training as failed")
            training.update(status=V1TrainingStatus.FAILED)
        raise
    finally:
        # --- Ensure Adapter is Unloaded in Finally Block ---
        # This handles cases where errors occur after adapter loading but before the explicit unload
        if (
            model_to_train
            and hasattr(model_to_train, "unload")
            and hasattr(model_to_train, "active_adapter")
        ):
            # Check if the adapter we intended to train is still active before unloading
            try:
                if model_to_train.active_adapter == adapter_name_for_peft:
                    print(
                        f"Ensuring adapter '{adapter_name_for_peft}' is unloaded in finally block..."
                    )
                    # model_to_train.to('cpu') # Optional precaution
                    model_to_train.unload()
                    print(
                        f"Adapter '{adapter_name_for_peft}' unloaded in finally block."
                    )
                else:
                    print(
                        f"Adapter '{adapter_name_for_peft}' was not the active adapter ({model_to_train.active_adapter}) in finally block, skipping unload."
                    )
            except Exception as final_unload_e:
                print(
                    f"Warning: Failed to unload adapter '{adapter_name_for_peft}' in finally block: {final_unload_e}"
                )
        # -------------------------------------------------

        # Additional cleanup in finally block
        model_to_train = None  # Clear reference again
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
        print(f"finally block cleanup finished. {training=} {failure=}")

        # Update training status based on final outcome ONLY IF training object exists
        if training:
            # If an exception occurred (failure=True), status is already FAILED.
            # If no exception occurred (!failure), we mark as COMPLETED.
            # This prevents overwriting FAILED status with COMPLETED in case of success path error before return
            if not failure:
                print("\n >> marking final training as completed in finally block")
                # Simply update; let the backend handle idempotency if needed
                training.update(status=V1TrainingStatus.COMPLETED)
                print("Updated Training status to COMPLETED in finally block.")
            else:
                print("\n >> Training marked as FAILED in except block")


def UnslothSFT(
    platform: str = "runpod",
    accelerators: List[str] = ["1:A100_SXM"],
    image: str = "pytorch/pytorch:2.6.0-cuda12.6-cudnn9-devel",
    scale: V1Scale = scale,
    namespace: Optional[str] = None,
    env: Optional[List[V1EnvVar]] = None,
    config: Optional[NebuGlobalConfig] = None,
    hot_reload: bool = True,
    debug: bool = False,
) -> Processor[TrainingRequest, TrainingResponse]:
    decorate = processor(
        image=image,
        setup_script=setup_script,
        accelerators=accelerators,
        platform=platform,
        scale=scale,
        namespace=namespace,
        env=env,
        # execution_mode="subprocess",
        config=config,
        hot_reload=hot_reload,
        debug=debug,
    )
    return decorate(train_unsloth_sft)
