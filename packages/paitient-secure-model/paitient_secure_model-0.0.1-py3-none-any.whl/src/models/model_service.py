"""
Model Service Module for Secure Model Service

This module provides functionality to download, manage, and configure 
AI models from HuggingFace, focusing on ZimaBlueAI/HuatuoGPT-o1-8B.
"""

import os
import json
import logging
import tempfile
from typing import Dict, Any, Optional, List, Tuple

import boto3
import torch
from huggingface_hub import snapshot_download
from transformers import AutoModelForCausalLM, AutoTokenizer
from safetensors import safe_open

from src.encryption.encryption_service import EncryptionService

logger = logging.getLogger(__name__)


class ModelService:
    """Service for downloading, storing, and managing AI models."""

    def __init__(
        self,
        client_id: str,
        s3_bucket: str,
        model_name: str = "ZimaBlueAI/HuatuoGPT-o1-8B",
        encryption_service: Optional[EncryptionService] = None,
    ):
        """
        Initialize the model service.

        Args:
            client_id: Unique identifier for the client
            s3_bucket: S3 bucket for model storage
            model_name: Name of the HuggingFace model to use
            encryption_service: Instance of EncryptionService for model encryption
        """
        self.client_id = client_id
        self.s3_bucket = s3_bucket
        self.model_name = model_name
        self.encryption_service = encryption_service or EncryptionService(client_id=client_id)
        
        # Initialize AWS clients
        self.s3_client = boto3.client("s3")
        
        # Model path in S3
        self.model_s3_prefix = f"models/{client_id}/{model_name.replace('/', '_')}"

    def download_model_from_huggingface(self, local_dir: Optional[str] = None) -> str:
        """
        Download a model from HuggingFace.

        Args:
            local_dir: Local directory to download the model to. If None, a temporary directory is used.

        Returns:
            Path to the downloaded model
        """
        if not local_dir:
            local_dir = tempfile.mkdtemp()
            
        logger.info(f"Downloading model {self.model_name} to {local_dir}")
        
        # Download model using huggingface_hub
        model_path = snapshot_download(
            repo_id=self.model_name,
            local_dir=local_dir,
            local_dir_use_symlinks=False
        )
        
        logger.info(f"Model downloaded to {model_path}")
        return model_path

    def extract_model_weights(self, model_path: str) -> Dict[str, Any]:
        """
        Extract model weights from downloaded files.

        Args:
            model_path: Path to the downloaded model

        Returns:
            Dictionary of model weights
        """
        logger.info(f"Extracting model weights from {model_path}")
        
        # Check if we have safetensors files
        safetensor_files = [f for f in os.listdir(model_path) if f.endswith('.safetensors')]
        
        if safetensor_files:
            # Extract weights from safetensors files
            weights = {}
            
            for sf in safetensor_files:
                file_path = os.path.join(model_path, sf)
                with safe_open(file_path, framework="pt") as f:
                    for k in f.keys():
                        # For large models, we don't want to load everything into memory at once
                        # So we just record the mapping of parameter names to files
                        weights[k] = {"file": sf, "key": k}
                        
            logger.info(f"Extracted weights metadata from {len(safetensor_files)} safetensors files")
            return weights
        else:
            # Load model as PyTorch model and extract weights
            logger.info("No safetensors found, loading as PyTorch model")
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True
            )
            
            # Convert model weights to dictionary
            weights = {name: param.detach().cpu().numpy().tolist() for name, param in model.state_dict().items()}
            
            logger.info(f"Extracted {len(weights)} weight tensors from PyTorch model")
            return weights

    def encrypt_and_upload_model(
        self,
        model_path: Optional[str] = None,
        encryption_password: Optional[str] = None,
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Encrypt model weights and upload to S3.

        Args:
            model_path: Path to the downloaded model. If None, the model will be downloaded.
            encryption_password: Optional password for additional encryption security

        Returns:
            Tuple of (S3 model key, encryption metadata)
        """
        # Download model if needed
        if not model_path:
            model_path = self.download_model_from_huggingface()
            
        # Extract model weights
        weights = self.extract_model_weights(model_path)
        
        logger.info(f"Encrypting model weights for client {self.client_id}")
        
        # Encrypt weights
        encrypted_weights, encryption_metadata = self.encryption_service.encrypt_model_weights(
            weights, password=encryption_password
        )
        
        # Upload encrypted weights to S3
        model_key = f"{self.model_s3_prefix}/encrypted_weights.json"
        self.s3_client.put_object(
            Bucket=self.s3_bucket,
            Key=model_key,
            Body=json.dumps(encrypted_weights),
            ContentType="application/json",
            Metadata={
                "client_id": self.client_id,
                "model_name": self.model_name,
                "encrypted": "true"
            }
        )
        
        # Upload encryption metadata to S3
        metadata_key = f"{self.model_s3_prefix}/encryption_metadata.json"
        self.s3_client.put_object(
            Bucket=self.s3_bucket,
            Key=metadata_key,
            Body=json.dumps(encryption_metadata),
            ContentType="application/json",
            Metadata={
                "client_id": self.client_id,
                "model_name": self.model_name,
                "content_type": "encryption_metadata"
            }
        )
        
        logger.info(f"Encrypted model uploaded to s3://{self.s3_bucket}/{model_key}")
        
        # Also upload model configuration and tokenizer
        self._upload_model_config_and_tokenizer(model_path)
        
        return model_key, encryption_metadata

    def _upload_model_config_and_tokenizer(self, model_path: str) -> None:
        """
        Upload model configuration and tokenizer to S3.

        Args:
            model_path: Path to the downloaded model
        """
        # Upload configuration file
        config_file = os.path.join(model_path, "config.json")
        if os.path.exists(config_file):
            self.s3_client.upload_file(
                Filename=config_file,
                Bucket=self.s3_bucket,
                Key=f"{self.model_s3_prefix}/config.json",
                ExtraArgs={
                    "Metadata": {
                        "client_id": self.client_id,
                        "model_name": self.model_name,
                        "content_type": "config"
                    }
                }
            )
        
        # Upload tokenizer files
        tokenizer_files = [
            "tokenizer.json",
            "tokenizer_config.json",
            "special_tokens_map.json",
            "vocab.json",
            "merges.txt"
        ]
        
        for tf in tokenizer_files:
            tokenizer_file = os.path.join(model_path, tf)
            if os.path.exists(tokenizer_file):
                self.s3_client.upload_file(
                    Filename=tokenizer_file,
                    Bucket=self.s3_bucket,
                    Key=f"{self.model_s3_prefix}/{tf}",
                    ExtraArgs={
                        "Metadata": {
                            "client_id": self.client_id,
                            "model_name": self.model_name,
                            "content_type": "tokenizer"
                        }
                    }
                )

    def download_encrypted_model(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Download encrypted model from S3.

        Returns:
            Tuple of (encrypted_weights, encryption_metadata)
        """
        try:
            # Download encrypted weights
            encrypted_weights_response = self.s3_client.get_object(
                Bucket=self.s3_bucket,
                Key=f"{self.model_s3_prefix}/encrypted_weights.json"
            )
            encrypted_weights = json.loads(encrypted_weights_response["Body"].read())
            
            # Download encryption metadata
            encryption_metadata_response = self.s3_client.get_object(
                Bucket=self.s3_bucket,
                Key=f"{self.model_s3_prefix}/encryption_metadata.json"
            )
            encryption_metadata = json.loads(encryption_metadata_response["Body"].read())
            
            return encrypted_weights, encryption_metadata
            
        except Exception as e:
            logger.error(f"Error downloading encrypted model: {str(e)}")
            raise

    def decrypt_model(
        self,
        encrypted_weights: Optional[Dict[str, Any]] = None,
        encryption_metadata: Optional[Dict[str, Any]] = None,
        encryption_password: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Decrypt model weights.

        Args:
            encrypted_weights: Encrypted model weights
            encryption_metadata: Metadata from encryption process
            encryption_password: Optional password matching the one used for encryption

        Returns:
            Decrypted model weights
        """
        # Download encrypted model if needed
        if not encrypted_weights or not encryption_metadata:
            encrypted_weights, encryption_metadata = self.download_encrypted_model()
        
        logger.info(f"Decrypting model weights for client {self.client_id}")
        
        # Decrypt weights
        decrypted_weights = self.encryption_service.decrypt_model_weights(
            encrypted_weights, encryption_metadata, password=encryption_password
        )
        
        return decrypted_weights

    def load_model_from_decrypted_weights(
        self,
        decrypted_weights: Optional[Dict[str, Any]] = None,
        encryption_password: Optional[str] = None,
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
    ) -> Tuple[Any, Any]:
        """
        Load a model from decrypted weights.

        Args:
            decrypted_weights: Decrypted model weights
            encryption_password: Optional password for decryption
            device: Device to load the model on

        Returns:
            Tuple of (model, tokenizer)
        """
        # Get decrypted weights if needed
        if not decrypted_weights:
            decrypted_weights = self.decrypt_model(encryption_password=encryption_password)
            
        # Download model configuration and tokenizer from S3
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Download config.json
            try:
                self.s3_client.download_file(
                    Bucket=self.s3_bucket,
                    Key=f"{self.model_s3_prefix}/config.json",
                    Filename=os.path.join(tmp_dir, "config.json")
                )
            except Exception as e:
                logger.error(f"Error downloading config.json: {str(e)}")
                raise
                
            # Download tokenizer files
            tokenizer_files = [
                "tokenizer.json",
                "tokenizer_config.json",
                "special_tokens_map.json",
                "vocab.json",
                "merges.txt"
            ]
            
            for tf in tokenizer_files:
                try:
                    self.s3_client.download_file(
                        Bucket=self.s3_bucket,
                        Key=f"{self.model_s3_prefix}/{tf}",
                        Filename=os.path.join(tmp_dir, tf)
                    )
                except Exception:
                    logger.warning(f"Tokenizer file {tf} not found, continuing...")
            
            # Load model and tokenizer
            model = AutoModelForCausalLM.from_config(
                os.path.join(tmp_dir, "config.json")
            )
            
            # Load weights into model
            state_dict = {k: torch.tensor(v) for k, v in decrypted_weights.items()}
            model.load_state_dict(state_dict)
            model.to(device)
            
            # Load tokenizer
            tokenizer = AutoTokenizer.from_pretrained(tmp_dir)
            
            return model, tokenizer
