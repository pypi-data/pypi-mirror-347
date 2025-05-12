"""
LoRA Fine-Tuning Service for Secure Model Service

This module provides functionality for LoRA (Low-Rank Adaptation) fine-tuning
of models for customization to client-specific needs.
"""

import os
import logging
import tempfile
import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

import torch
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    TaskType
)
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset

logger = logging.getLogger(__name__)


class LoraFineTuningService:
    """Service for LoRA fine-tuning of language models."""

    def __init__(
        self,
        client_id: str,
        model_dir: Optional[str] = None,
        output_dir: Optional[str] = None
    ):
        """
        Initialize the LoRA fine-tuning service.

        Args:
            client_id: Unique identifier for the client
            model_dir: Directory containing the base model
            output_dir: Directory to save fine-tuned models
        """
        self.client_id = client_id
        self.model_dir = model_dir
        
        # Default output directory if not specified
        if output_dir is None:
            output_dir = f"./models/{client_id}/lora"
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)

    def prepare_model_for_training(
        self,
        model_path: Union[str, Path],
        load_in_8bit: bool = False,
        device_map: Optional[str] = "auto"
    ) -> tuple:
        """
        Load and prepare a model for LoRA fine-tuning.

        Args:
            model_path: Path to the model directory
            load_in_8bit: Whether to load the model in 8-bit precision
            device_map: Device mapping strategy

        Returns:
            Tuple of (model, tokenizer)
        """
        logger.info(f"Loading model from {model_path} for LoRA fine-tuning")
        
        # Determine compute dtype based on available hardware
        compute_dtype = torch.float16
        if torch.cuda.is_available() and torch.cuda.get_device_capability()[0] >= 8:
            logger.info("Using BFloat16 precision (detected Ampere or newer GPU)")
            compute_dtype = torch.bfloat16
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        # Ensure the tokenizer has a pad token
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            logger.info(f"Setting pad_token to eos_token: {tokenizer.eos_token}")
        
        # Load model with optimizations
        load_kwargs = {
            "torch_dtype": compute_dtype,
            "device_map": device_map
        }
        
        if load_in_8bit:
            logger.info("Loading model in 8-bit precision")
            load_kwargs["load_in_8bit"] = True
        
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            **load_kwargs
        )
        
        # Prepare for training
        if load_in_8bit:
            model = prepare_model_for_kbit_training(model)
        
        return model, tokenizer

    def configure_lora(
        self,
        model: Any,
        lora_rank: int = 8,
        lora_alpha: int = 16,
        lora_dropout: float = 0.05,
        target_modules: Optional[List[str]] = None
    ) -> Any:
        """
        Apply LoRA configuration to the model.

        Args:
            model: The model to configure for LoRA
            lora_rank: Rank of the LoRA matrices
            lora_alpha: LoRA alpha parameter
            lora_dropout: Dropout probability for LoRA
            target_modules: List of modules to apply LoRA to

        Returns:
            LoRA-configured model
        """
        # If target modules not specified, use defaults based on model type
        if target_modules is None:
            # Check model architecture to determine target modules
            if hasattr(model, "get_base_model") and hasattr(model.get_base_model(), "model"):
                if "GPTNeoX" in model.config.architectures[0]:
                    target_modules = ["query_key_value", "dense", "dense_h_to_4h", "dense_4h_to_h"]
                elif "LlamaForCausalLM" in model.config.architectures[0]:
                    target_modules = ["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
                elif "MPTForCausalLM" in model.config.architectures[0]:
                    target_modules = ["Wqkv", "out_proj", "fc1", "fc2"]
                else:
                    # Default for most architectures
                    target_modules = ["c_attn", "c_proj", "c_fc", "c_proj"]
        
        logger.info(f"Configuring LoRA with rank={lora_rank}, alpha={lora_alpha}")
        logger.info(f"Target modules: {target_modules}")
        
        # Create LoRA config
        lora_config = LoraConfig(
            r=lora_rank,
            lora_alpha=lora_alpha,
            target_modules=target_modules,
            lora_dropout=lora_dropout,
            bias="none",
            task_type=TaskType.CAUSAL_LM
        )
        
        # Apply LoRA to the model
        model = get_peft_model(model, lora_config)
        
        # Print trainable parameters info
        model.print_trainable_parameters()
        
        return model

    def prepare_dataset(
        self,
        dataset_path: str,
        tokenizer: Any,
        max_length: int = 1024,
        text_column: str = "text"
    ) -> Any:
        """
        Prepare a dataset for fine-tuning.

        Args:
            dataset_path: Path or identifier of the dataset
            tokenizer: Tokenizer to use for encoding
            max_length: Maximum sequence length
            text_column: Column containing the text data

        Returns:
            Processed dataset
        """
        logger.info(f"Preparing dataset from {dataset_path}")
        
        # Load dataset
        if dataset_path.startswith(("s3://", "http://", "https://")):
            # Load from URL or S3
            with tempfile.NamedTemporaryFile(mode="w+", suffix=".jsonl", delete=False) as tmp:
                # In a real implementation, download from URL or S3
                # For now, create a small synthetic dataset
                sample_data = [
                    {"text": "This is a sample text for fine-tuning."},
                    {"text": "The model will be customized for the client."}
                ]
                for item in sample_data:
                    tmp.write(json.dumps(item) + "\n")
                
                dataset_path = tmp.name
                logger.info(f"Created temporary dataset at {dataset_path}")
        
        # Load the dataset
        if dataset_path.endswith(".jsonl"):
            dataset = load_dataset("json", data_files=dataset_path)
        elif dataset_path.endswith(".csv"):
            dataset = load_dataset("csv", data_files=dataset_path)
        elif dataset_path.endswith(".txt"):
            with open(dataset_path, "r") as f:
                lines = f.readlines()
                data = [{"text": line.strip()} for line in lines if line.strip()]
                with tempfile.NamedTemporaryFile(mode="w+", suffix=".jsonl", delete=False) as tmp:
                    for item in data:
                        tmp.write(json.dumps(item) + "\n")
                    dataset = load_dataset("json", data_files=tmp.name)
        else:
            # Try to load as a HuggingFace dataset
            try:
                dataset = load_dataset(dataset_path)
            except Exception as e:
                logger.error(f"Failed to load dataset: {str(e)}")
                raise
        
        # Preprocess function
        def preprocess_function(examples):
            return tokenizer(
                examples[text_column],
                truncation=True,
                max_length=max_length,
                padding="max_length"
            )
            
        # Apply preprocessing
        tokenized_dataset = dataset.map(
            preprocess_function,
            batched=True,
            remove_columns=[col for col in dataset["train"].column_names if col != text_column]
        )
        
        return tokenized_dataset

    def train(
        self,
        model_path: Union[str, Path],
        dataset_path: str,
        output_dir: Optional[Union[str, Path]] = None,
        lora_rank: int = 8,
        learning_rate: float = 2e-4,
        batch_size: int = 8,
        num_epochs: int = 3,
        max_length: int = 1024,
        load_in_8bit: bool = False
    ) -> str:
        """
        Fine-tune a model using LoRA.

        Args:
            model_path: Path to the model directory
            dataset_path: Path or identifier of the dataset
            output_dir: Directory to save the fine-tuned model
            lora_rank: Rank of the LoRA matrices
            learning_rate: Learning rate for training
            batch_size: Batch size for training
            num_epochs: Number of training epochs
            max_length: Maximum sequence length
            load_in_8bit: Whether to load the model in 8-bit precision

        Returns:
            Path to the fine-tuned model
        """
        if output_dir is None:
            output_dir = self.output_dir / Path(model_path).name.replace("/", "_")
        else:
            output_dir = Path(output_dir)
            
        output_dir.mkdir(exist_ok=True, parents=True)
        
        logger.info(f"Starting LoRA fine-tuning")
        logger.info(f"Model: {model_path}")
        logger.info(f"Dataset: {dataset_path}")
        logger.info(f"Output directory: {output_dir}")
        
        # Load and prepare model
        model, tokenizer = self.prepare_model_for_training(model_path, load_in_8bit)
        
        # Configure LoRA
        model = self.configure_lora(model, lora_rank=lora_rank)
        
        # Prepare dataset
        tokenized_dataset = self.prepare_dataset(dataset_path, tokenizer, max_length)
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer, 
            mlm=False
        )
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=str(output_dir),
            learning_rate=learning_rate,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=4,
            num_train_epochs=num_epochs,
            weight_decay=0.01,
            logging_steps=10,
            save_steps=100,
            save_total_limit=3,
            report_to="none",
            push_to_hub=False
        )
        
        # Initialize trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset["train"],
            data_collator=data_collator
        )
        
        # Start training
        logger.info("Starting training")
        trainer.train()
        
        # Save model
        logger.info(f"Saving model to {output_dir}")
        model.save_pretrained(output_dir)
        tokenizer.save_pretrained(output_dir)
        
        return str(output_dir)

    def encrypt_and_upload_lora_adapter(
        self, 
        adapter_path: Union[str, Path],
        encryption_service: Any,
        s3_client: Any,
        s3_bucket: str,
        password: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Encrypt and upload LoRA adapter weights.

        Args:
            adapter_path: Path to the LoRA adapter
            encryption_service: Encryption service for securing weights
            s3_client: AWS S3 client
            s3_bucket: S3 bucket name
            password: Optional password for encryption

        Returns:
            Dictionary with upload information
        """
        adapter_path = Path(adapter_path)
        logger.info(f"Encrypting and uploading LoRA adapter from {adapter_path}")
        
        # Load adapter config
        with open(adapter_path / "adapter_config.json", "r") as f:
            adapter_config = json.load(f)
            
        # Load adapter weights
        adapter_weights = {}
        for weights_file in (adapter_path / "adapter_model").glob("*.bin"):
            weights_tensor = torch.load(weights_file, map_location="cpu")
            for key, tensor in weights_tensor.items():
                adapter_weights[key] = tensor.cpu().numpy().tolist()
                
        # Encrypt adapter weights
        encrypted_weights, encryption_metadata = encryption_service.encrypt_model_weights(
            adapter_weights, password=password
        )
        
        # Create temporary files for encrypted data
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as weights_file:
            json.dump(encrypted_weights, weights_file)
            weights_file_path = weights_file.name
            
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as metadata_file:
            json.dump(encryption_metadata, metadata_file)
            metadata_file_path = metadata_file.name
            
        # Upload to S3
        s3_prefix = f"clients/{self.client_id}/lora/{adapter_path.name}"
        
        # Upload encrypted weights
        weights_key = f"{s3_prefix}/encrypted_weights.json"
        s3_client.upload_file(
            weights_file_path,
            s3_bucket,
            weights_key,
            ExtraArgs={"ServerSideEncryption": "AES256"}
        )
        
        # Upload encryption metadata
        metadata_key = f"{s3_prefix}/encryption_metadata.json"
        s3_client.upload_file(
            metadata_file_path,
            s3_bucket,
            metadata_key,
            ExtraArgs={"ServerSideEncryption": "AES256"}
        )
        
        # Upload adapter config
        config_key = f"{s3_prefix}/adapter_config.json"
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as config_file:
            json.dump(adapter_config, config_file)
            s3_client.upload_file(
                config_file.name,
                s3_bucket,
                config_key,
                ExtraArgs={"ServerSideEncryption": "AES256"}
            )
            
        # Clean up temporary files
        os.unlink(weights_file_path)
        os.unlink(metadata_file_path)
        os.unlink(config_file.name)
        
        return {
            "s3_bucket": s3_bucket,
            "s3_prefix": s3_prefix,
            "adapter_name": adapter_path.name,
            "client_id": self.client_id
        }
