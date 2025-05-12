#!/usr/bin/env python3
"""
Secure Model Service CLI

This script provides a command-line interface for deploying and managing
secure model endpoints for clients.
"""

import os
import sys
import logging
import argparse
import json
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add project root to Python path
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
))

from src.aws.aws_service import AWSService
from src.models.model_service import ModelService
from src.encryption.encryption_service import EncryptionService
from src.kubernetes.kubernetes_service import KubernetesService
from src.models.lora_service import LoraFineTuningService
from src.core.config_service import get_config_service


def setup_logging(debug: bool = False):
    """Set up logging configuration."""
    level = logging.DEBUG if debug else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('secure_model_cli.log')
        ]
    )
    
    return logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Secure Model Service CLI')
    
    # Global options
    parser.add_argument(
        '--client-id',
        type=str,
        required=True,
        help='Client ID for the deployment'
    )
    
    parser.add_argument(
        '--environment',
        type=str,
        default='dev',
        choices=['dev', 'staging', 'prod'],
        help='Deployment environment'
    )
    
    parser.add_argument(
        '--region',
        type=str,
        help='AWS region (defaults to AWS_REGION env var)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    parser.add_argument(
        '--config-file',
        type=str,
        help='Path to configuration file'
    )
    
    # Subparsers for commands
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy a model')
    deploy_parser.add_argument(
        '--model-name',
        type=str,
        default='ZimaBlueAI/HuatuoGPT-o1-8B',
        help='Model name from HuggingFace'
    )
    deploy_parser.add_argument(
        '--gpu-count',
        type=int,
        default=1,
        help='Number of GPUs to allocate'
    )
    deploy_parser.add_argument(
        '--deployment-type',
        type=str,
        choices=['kubernetes', 'ec2', 'auto'],
        default='auto',
        help='Deployment type'
    )
    deploy_parser.add_argument(
        '--enable-lora',
        action='store_true',
        help='Enable LoRA fine-tuning'
    )
    deploy_parser.add_argument(
        '--encryption-password',
        type=str,
        help='Password for encryption (if not using KMS)'
    )
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a deployment')
    delete_parser.add_argument(
        '--deployment-id',
        type=str,
        help='Deployment ID to delete'
    )
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Get deployment status')
    status_parser.add_argument(
        '--deployment-id',
        type=str,
        help='Deployment ID to check'
    )
    
    # Finetune command
    finetune_parser = subparsers.add_parser('finetune', help='Run LoRA fine-tuning')
    finetune_parser.add_argument(
        '--dataset-path',
        type=str,
        required=True,
        help='Path or URL to dataset'
    )
    finetune_parser.add_argument(
        '--deployment-id',
        type=str,
        help='Deployment ID to fine-tune'
    )
    finetune_parser.add_argument(
        '--lora-rank',
        type=int,
        default=8,
        help='LoRA rank'
    )
    finetune_parser.add_argument(
        '--num-epochs',
        type=int,
        default=3,
        help='Number of training epochs'
    )
    
    return parser.parse_args()


def find_deployment_id(client_id: str, aws_service: AWSService) -> Optional[str]:
    """
    Find a deployment ID for a client.
    
    In a full implementation, this would query a database.
    For now, we use a simple heuristic.
    """
    # Simple heuristic - use the CloudFormation stack ID
    return f"deploy-{client_id}-{os.urandom(4).hex()}"


def deploy_model(args, logger, config):
    """Deploy a model for a client."""
    logger.info(f"Deploying model {args.model_name} for client {args.client_id}")
    
    # Create AWS service
    aws_service = AWSService(
        client_id=args.client_id,
        environment=args.environment,
        region=args.region or config.get('aws.region')
    )
    
    # Create S3 resources
    logger.info("Creating S3 resources...")
    s3_resources = aws_service.create_s3_resources()
    logger.info(f"S3 resources created: {json.dumps(s3_resources, indent=2)}")
    
    # Create encryption service
    encryption_service = EncryptionService(
        kms_key_arn=s3_resources.get('encryption_key_arn'),
        client_id=args.client_id
    )
    
    # Create model service
    model_service = ModelService(
        client_id=args.client_id,
        s3_bucket=s3_resources.get('client_bucket'),
        model_name=args.model_name,
        encryption_service=encryption_service
    )
    
    # Download, encrypt, and upload model
    logger.info(f"Downloading and encrypting model {args.model_name}...")
    model_key, encryption_metadata = model_service.encrypt_and_upload_model(
        encryption_password=args.encryption_password
    )
    logger.info(f"Model encrypted and uploaded to {model_key}")
    
    # Determine deployment type
    deployment_type = args.deployment_type
    if deployment_type == 'auto':
        # Check if kubectl is available
        import subprocess
        try:
            subprocess.run(['kubectl', 'version'], capture_output=True, check=True)
            deployment_type = 'kubernetes'
        except (subprocess.SubprocessError, FileNotFoundError):
            deployment_type = 'ec2'
    
    if deployment_type == 'kubernetes':
        # Deploy to Kubernetes
        logger.info("Deploying to Kubernetes...")
        k8s_service = KubernetesService(
            namespace=f"client-{args.client_id}",
            config_dir=str(Path(__file__).parent.parent / "config" / "kubernetes")
        )
        
        # Get ECR repository URI - in a real implementation, this would be properly set up
        ecr_repo_uri = f"{s3_resources.get('aws_account_id')}.dkr.ecr.{args.region or config.get('aws.region')}.amazonaws.com/secure-model-service"
        
        deployment = k8s_service.deploy_model_service(
            client_id=args.client_id,
            model_name=args.model_name,
            image_uri=ecr_repo_uri,
            gpu_count=args.gpu_count,
            s3_bucket=s3_resources.get('client_bucket'),
            encryption_key_arn=s3_resources.get('encryption_key_arn')
        )
        
        logger.info(f"Kubernetes deployment created: {json.dumps(deployment, indent=2)}")
        
        # Create deployment record
        deployment_id = f"k8s-{args.client_id}-{os.urandom(4).hex()}"
        endpoint = deployment.get('endpoint')
        
    else:
        # Deploy to EC2
        logger.info("Deploying to EC2...")
        
        # Create EC2 resources
        ec2_resources = aws_service.create_ec2_resources(
            instance_type=f"g4dn.{args.gpu_count}xlarge" if args.gpu_count > 1 else "g4dn.xlarge"
        )
        logger.info(f"EC2 resources created: {json.dumps(ec2_resources, indent=2)}")
        
        # Create Lambda endpoint
        logger.info("Creating Lambda endpoint...")
        lambda_resources = aws_service.create_lambda_resources(
            model_service_endpoint=ec2_resources.get('public_ip') or ec2_resources.get('elastic_ip')
        )
        logger.info(f"Lambda endpoint created: {json.dumps(lambda_resources, indent=2)}")
        
        # Create deployment record
        deployment_id = f"ec2-{args.client_id}-{os.urandom(4).hex()}"
        endpoint = lambda_resources.get('api_endpoint')
        api_key = lambda_resources.get('api_key_value')
    
    # Return deployment info
    return {
        'deployment_id': deployment_id,
        'client_id': args.client_id,
        'model_name': args.model_name,
        'status': 'active',
        'endpoint': endpoint,
        'api_key': api_key if 'api_key' in locals() else None,
        'deployment_type': deployment_type,
        'model_key': model_key,
        'enable_lora': args.enable_lora
    }


def delete_deployment(args, logger, config):
    """Delete a deployment."""
    logger.info(f"Deleting deployment {args.deployment_id} for client {args.client_id}")
    
    # In a full implementation, we would look up the deployment details
    # from a database and then delete the resources
    
    # For now, we just determine the deployment type from the ID prefix
    deployment_type = args.deployment_id.split('-')[0]
    
    # Create AWS service
    aws_service = AWSService(
        client_id=args.client_id,
        environment=args.environment,
        region=args.region or config.get('aws.region')
    )
    
    if deployment_type == 'k8s':
        # Delete Kubernetes resources
        logger.info("Deleting Kubernetes resources...")
        k8s_service = KubernetesService(
            namespace=f"client-{args.client_id}",
            config_dir=str(Path(__file__).parent.parent / "config" / "kubernetes")
        )
        
        result = k8s_service.delete_model_service(args.client_id)
        logger.info(f"Kubernetes resources deleted: {json.dumps(result, indent=2)}")
    else:
        # Delete EC2 and Lambda resources
        # In a real implementation, we would delete the CloudFormation stacks
        logger.info("Deleting EC2 and Lambda resources...")
        logger.info("(Not implemented in this demo)")
    
    return {
        'deployment_id': args.deployment_id,
        'client_id': args.client_id,
        'status': 'deleted'
    }


def get_deployment_status(args, logger, config):
    """Get deployment status."""
    logger.info(f"Getting status for deployment {args.deployment_id} for client {args.client_id}")
    
    # In a full implementation, we would look up the deployment details
    # from a database and check the actual resources
    
    # For now, we just determine the deployment type from the ID prefix
    deployment_type = args.deployment_id.split('-')[0]
    
    if deployment_type == 'k8s':
        # Check Kubernetes resources
        logger.info("Checking Kubernetes resources...")
        k8s_service = KubernetesService(
            namespace=f"client-{args.client_id}",
            config_dir=str(Path(__file__).parent.parent / "config" / "kubernetes")
        )
        
        status = k8s_service.get_service_status(args.client_id)
        logger.info(f"Kubernetes status: {json.dumps(status, indent=2)}")
        
        return {
            'deployment_id': args.deployment_id,
            'client_id': args.client_id,
            'status': 'active' if status.get('status') == 'found' else 'not_found',
            'details': status
        }
    else:
        # Check EC2 and Lambda resources
        # In a real implementation, we would check the CloudFormation stacks
        logger.info("Checking EC2 and Lambda resources...")
        logger.info("(Not implemented in this demo - assuming active)")
        
        return {
            'deployment_id': args.deployment_id,
            'client_id': args.client_id,
            'status': 'active',
            'details': {
                'message': 'Status check not implemented in this demo'
            }
        }


def run_lora_finetune(args, logger, config):
    """Run LoRA fine-tuning."""
    logger.info(f"Fine-tuning model for client {args.client_id} with dataset {args.dataset_path}")
    
    # In a full implementation, we would look up the deployment details
    # and get the model information
    
    # Create AWS service
    aws_service = AWSService(
        client_id=args.client_id,
        environment=args.environment,
        region=args.region or config.get('aws.region')
    )
    
    # Determine S3 bucket
    s3_bucket = f"secure-model-service-{args.client_id}-{args.environment}"
    
    # Create encryption service
    encryption_service = EncryptionService(
        client_id=args.client_id
    )
    
    # Create LoRA service
    lora_service = LoraFineTuningService(
        client_id=args.client_id,
        output_dir=f"./models/{args.client_id}/lora"
    )
    
    # Run fine-tuning (in a real implementation, this would be done in the background)
    logger.info("Starting LoRA fine-tuning...")
    logger.info("Note: In this demo, we don't actually run the fine-tuning as it requires GPU resources")
    
    # Mock fine-tuning result
    job_id = f"lora-job-{args.client_id}-{os.urandom(4).hex()}"
    
    return {
        'job_id': job_id,
        'client_id': args.client_id,
        'dataset_path': args.dataset_path,
        'lora_rank': args.lora_rank,
        'num_epochs': args.num_epochs,
        'status': 'submitted'
    }


def main():
    """Main function."""
    args = parse_args()
    logger = setup_logging(args.debug)
    
    logger.info(f"Secure Model Service CLI - Command: {args.command}")
    
    # Load configuration
    config = get_config_service(
        env_file=".env",
        config_dir="config",
        environment=args.environment
    )
    
    # Execute command
    try:
        if args.command == 'deploy':
            result = deploy_model(args, logger, config)
        elif args.command == 'delete':
            result = delete_deployment(args, logger, config)
        elif args.command == 'status':
            result = get_deployment_status(args, logger, config)
        elif args.command == 'finetune':
            result = run_lora_finetune(args, logger, config)
        else:
            logger.error(f"Unknown command: {args.command}")
            return 1
        
        # Output result as JSON
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        logger.exception(f"Error executing command: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
