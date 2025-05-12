#!/usr/bin/env python3
"""
Secure Model Client

Main client interface for the Secure Model Service SDK.
"""

import os
import json
import time
import logging
import requests
from typing import Dict, List, Any, Optional, Union

from .core.config_service import load_config

logger = logging.getLogger(__name__)

class SecureModelClient:
    """
    Client for interacting with the Secure Model Service.
    
    This client provides a high-level interface for:
    - Deploying encrypted models
    - Generating text from deployed models
    - Managing model deployments
    - Checking subscription status
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        client_id: Optional[str] = None,
        endpoint: Optional[str] = None,
        config_path: Optional[str] = None,
        environment: str = "dev"
    ):
        """
        Initialize the Secure Model Client.
        
        Args:
            api_key: API key for authentication (can also be set via SECURE_MODEL_API_KEY env var)
            client_id: Client ID (can also be set via SECURE_MODEL_CLIENT_ID env var)
            endpoint: API endpoint (can also be set via SECURE_MODEL_ENDPOINT env var)
            config_path: Path to configuration file
            environment: Environment (dev, staging, prod)
        """
        # Load configuration
        self.config = load_config(config_path=config_path, environment=environment)
        
        # Set API key from argument, environment, or config
        self.api_key = api_key or os.environ.get("SECURE_MODEL_API_KEY") or self.config.get("api", {}).get("key")
        if not self.api_key:
            raise ValueError("API key must be provided via argument, SECURE_MODEL_API_KEY env var, or config")
        
        # Set client ID from argument, environment, or config
        self.client_id = client_id or os.environ.get("SECURE_MODEL_CLIENT_ID") or self.config.get("client", {}).get("id")
        if not self.client_id:
            raise ValueError("Client ID must be provided via argument, SECURE_MODEL_CLIENT_ID env var, or config")
        
        # Set endpoint from argument, environment, or config
        self.endpoint = endpoint or os.environ.get("SECURE_MODEL_ENDPOINT") or self.config.get("api", {}).get("endpoint")
        if not self.endpoint:
            # Default endpoint based on environment
            if environment == "prod":
                self.endpoint = "https://api.securemodel.ai/v1"
            elif environment == "staging":
                self.endpoint = "https://api-staging.securemodel.ai/v1"
            else:
                self.endpoint = "https://api-dev.securemodel.ai/v1"
        
        # Set session
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Client-ID": self.client_id
        })
        
        logger.info(f"Initialized Secure Model Client for client ID: {self.client_id}")
    
    def deploy(
        self,
        model_name: str,
        tier: str = "basic",
        use_gpu: bool = False,
        instance_type: Optional[str] = None,
        region: Optional[str] = None,
        environment: Optional[str] = None,
        custom_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Deploy a secure model.
        
        Args:
            model_name: Name of the model to deploy
            tier: Subscription tier (basic, pro, enterprise)
            use_gpu: Whether to use GPU
            instance_type: EC2 instance type or Kubernetes resources
            region: AWS region
            environment: Deployment environment
            custom_config: Additional configuration options
            
        Returns:
            Deployment information
        """
        logger.info(f"Deploying model {model_name} (tier: {tier}, GPU: {use_gpu})")
        
        # Build request payload
        payload = {
            "model_name": model_name,
            "tier": tier,
            "use_gpu": use_gpu,
            "client_id": self.client_id
        }
        
        # Add optional parameters
        if instance_type:
            payload["instance_type"] = instance_type
        
        if region:
            payload["region"] = region
        
        if environment:
            payload["environment"] = environment
        
        if custom_config:
            payload.update(custom_config)
        
        # Send request
        response = self.session.post(
            f"{self.endpoint}/deployments",
            json=payload
        )
        
        # Handle response
        if response.status_code != 200:
            error_message = f"Deployment failed with status {response.status_code}: {response.text}"
            logger.error(error_message)
            raise Exception(error_message)
        
        deployment_data = response.json()
        logger.info(f"Deployment successful, ID: {deployment_data.get('deployment_id')}")
        
        return deployment_data
    
    def delete_deployment(self, deployment_id: str) -> Dict[str, Any]:
        """
        Delete a model deployment.
        
        Args:
            deployment_id: ID of the deployment to delete
            
        Returns:
            Deletion status
        """
        logger.info(f"Deleting deployment {deployment_id}")
        
        response = self.session.delete(
            f"{self.endpoint}/deployments/{deployment_id}"
        )
        
        # Handle response
        if response.status_code != 200:
            error_message = f"Deletion failed with status {response.status_code}: {response.text}"
            logger.error(error_message)
            raise Exception(error_message)
        
        result = response.json()
        logger.info(f"Deployment {deployment_id} deleted successfully")
        
        return result
    
    def get_deployment_status(self, deployment_id: str) -> Dict[str, Any]:
        """
        Get deployment status.
        
        Args:
            deployment_id: ID of the deployment
            
        Returns:
            Deployment status
        """
        logger.info(f"Getting status for deployment {deployment_id}")
        
        response = self.session.get(
            f"{self.endpoint}/deployments/{deployment_id}"
        )
        
        # Handle response
        if response.status_code != 200:
            error_message = f"Status check failed with status {response.status_code}: {response.text}"
            logger.error(error_message)
            raise Exception(error_message)
        
        status_data = response.json()
        logger.info(f"Deployment status: {status_data.get('status')}")
        
        return status_data
    
    def list_deployments(self) -> List[Dict[str, Any]]:
        """
        List all deployments for the client.
        
        Returns:
            List of deployments
        """
        logger.info("Listing deployments")
        
        response = self.session.get(
            f"{self.endpoint}/deployments"
        )
        
        # Handle response
        if response.status_code != 200:
            error_message = f"List deployments failed with status {response.status_code}: {response.text}"
            logger.error(error_message)
            raise Exception(error_message)
        
        deployments = response.json().get("deployments", [])
        logger.info(f"Found {len(deployments)} deployments")
        
        return deployments
    
    def generate(
        self,
        prompt: str,
        deployment_id: Optional[str] = None,
        max_tokens: int = 256,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 50,
        stop_sequences: Optional[List[str]] = None,
        repetition_penalty: Optional[float] = None,
        streaming: bool = False
    ) -> Union[Dict[str, Any], 'GenerationStream']:
        """
        Generate text from a deployed model.
        
        Args:
            prompt: Input prompt
            deployment_id: ID of the deployment to use (uses default if not specified)
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            top_p: Nucleus sampling parameter (0.0-1.0)
            top_k: Top-k sampling parameter
            stop_sequences: Sequences that stop generation
            repetition_penalty: Repetition penalty
            streaming: Whether to stream the response
            
        Returns:
            Generation result or stream
        """
        logger.info(f"Generating text (streaming: {streaming})")
        
        # Build request payload
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "streaming": streaming
        }
        
        # Add optional parameters
        if stop_sequences:
            payload["stop_sequences"] = stop_sequences
        
        if repetition_penalty:
            payload["repetition_penalty"] = repetition_penalty
        
        # Determine URL based on whether deployment_id is provided
        if deployment_id:
            url = f"{self.endpoint}/deployments/{deployment_id}/generate"
        else:
            url = f"{self.endpoint}/generate"
        
        # Handle streaming
        if streaming:
            from .utils.streaming import GenerationStream
            return GenerationStream(self.session, url, payload)
        
        # Send request
        response = self.session.post(url, json=payload)
        
        # Handle response
        if response.status_code != 200:
            error_message = f"Generation failed with status {response.status_code}: {response.text}"
            logger.error(error_message)
            raise Exception(error_message)
        
        result = response.json()
        
        if "text" in result:
            logger.info(f"Generated {len(result.get('text', ''))} characters")
        
        return result
    
    def finetune(
        self,
        base_model: str,
        dataset_path: str,
        deployment_id: Optional[str] = None,
        lora_rank: int = 8,
        learning_rate: float = 5e-5,
        num_epochs: int = 3,
        batch_size: int = 4
    ) -> Dict[str, Any]:
        """
        Run LoRA fine-tuning on a model.
        
        Args:
            base_model: Base model to fine-tune
            dataset_path: Path to dataset (local or S3)
            deployment_id: ID of the deployment to fine-tune (or create new if None)
            lora_rank: LoRA rank
            learning_rate: Learning rate
            num_epochs: Number of training epochs
            batch_size: Batch size
            
        Returns:
            Fine-tuning job information
        """
        logger.info(f"Starting fine-tuning job for {base_model}")
        
        # Build request payload
        payload = {
            "base_model": base_model,
            "dataset_path": dataset_path,
            "lora_rank": lora_rank,
            "learning_rate": learning_rate,
            "num_epochs": num_epochs,
            "batch_size": batch_size
        }
        
        # Add deployment_id if provided
        if deployment_id:
            payload["deployment_id"] = deployment_id
        
        # Send request
        response = self.session.post(
            f"{self.endpoint}/finetune",
            json=payload
        )
        
        # Handle response
        if response.status_code != 200:
            error_message = f"Fine-tuning failed with status {response.status_code}: {response.text}"
            logger.error(error_message)
            raise Exception(error_message)
        
        job_data = response.json()
        logger.info(f"Fine-tuning job started, ID: {job_data.get('job_id')}")
        
        return job_data
    
    def get_finetune_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get status of a fine-tuning job.
        
        Args:
            job_id: ID of the fine-tuning job
            
        Returns:
            Fine-tuning job status
        """
        logger.info(f"Getting status for fine-tuning job {job_id}")
        
        response = self.session.get(
            f"{self.endpoint}/finetune/{job_id}"
        )
        
        # Handle response
        if response.status_code != 200:
            error_message = f"Status check failed with status {response.status_code}: {response.text}"
            logger.error(error_message)
            raise Exception(error_message)
        
        status_data = response.json()
        logger.info(f"Fine-tuning job status: {status_data.get('status')}")
        
        return status_data
    
    def check_subscription(self) -> Dict[str, Any]:
        """
        Check subscription status.
        
        Returns:
            Subscription information
        """
        logger.info(f"Checking subscription for client {self.client_id}")
        
        response = self.session.get(
            f"{self.endpoint}/subscription"
        )
        
        # Handle response
        if response.status_code != 200:
            error_message = f"Subscription check failed with status {response.status_code}: {response.text}"
            logger.error(error_message)
            raise Exception(error_message)
        
        subscription_data = response.json()
        
        is_active = subscription_data.get("is_active", False)
        tier = subscription_data.get("subscription_tier", "none")
        
        logger.info(f"Subscription status: active={is_active}, tier={tier}")
        
        return subscription_data
    
    def close(self):
        """Close the client session."""
        self.session.close()
    
    def __enter__(self):
        """Support for context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support for context manager."""
        self.close()
