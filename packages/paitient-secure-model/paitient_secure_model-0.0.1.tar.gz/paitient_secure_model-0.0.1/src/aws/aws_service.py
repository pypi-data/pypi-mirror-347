"""
AWS Service Module for Secure Model Service

This module provides functionality for managing AWS resources including
S3 buckets, EC2 instances, and Lambda functions.
"""

import os
import json
import logging
import tempfile
from typing import Dict, Any, Optional, List, Union

import boto3
import botocore

logger = logging.getLogger(__name__)


class AWSService:
    """Service for managing AWS resources for the secure model service."""

    def __init__(
        self,
        client_id: str,
        environment: str = "dev",
        region: Optional[str] = None,
        aws_profile: Optional[str] = None,
        config_dir: str = "/app/config/aws",
    ):
        """
        Initialize the AWS service.

        Args:
            client_id: Unique identifier for the client
            environment: Deployment environment (dev, staging, prod)
            region: AWS region
            aws_profile: AWS profile to use
            config_dir: Directory containing AWS CloudFormation templates
        """
        self.client_id = client_id
        self.environment = environment
        self.config_dir = config_dir
        
        # Set up AWS session
        session_kwargs = {}
        if region:
            session_kwargs["region_name"] = region
        if aws_profile:
            session_kwargs["profile_name"] = aws_profile
            
        self.session = boto3.Session(**session_kwargs)
        self.region = self.session.region_name
        
        # Initialize AWS clients
        self.s3_client = self.session.client('s3')
        self.ec2_client = self.session.client('ec2')
        self.kms_client = self.session.client('kms')
        self.lambda_client = self.session.client('lambda')
        self.cloudformation_client = self.session.client('cloudformation')
        
        # S3 bucket names
        self.main_bucket = f"secure-model-service-{self.environment}"
        self.client_bucket = f"secure-model-service-{client_id}-{self.environment}"
        self.logs_bucket = f"secure-model-service-logs-{self.environment}"
        
    def create_s3_resources(self) -> Dict[str, Any]:
        """
        Create S3 buckets and related resources using CloudFormation.

        Returns:
            Dictionary with stack outputs
        """
        logger.info(f"Creating S3 resources for client {self.client_id}")
        
        template_path = os.path.join(self.config_dir, "s3-template.yaml")
        with open(template_path, 'r') as f:
            template_body = f.read()
        
        stack_name = f"secure-model-service-s3-{self.client_id}-{self.environment}"
        
        # Check if stack already exists
        try:
            self.cloudformation_client.describe_stacks(StackName=stack_name)
            stack_exists = True
        except botocore.exceptions.ClientError:
            stack_exists = False
            
        # Create or update stack
        parameters = [
            {'ParameterKey': 'ClientId', 'ParameterValue': self.client_id},
            {'ParameterKey': 'Environment', 'ParameterValue': self.environment}
        ]
        
        if stack_exists:
            response = self.cloudformation_client.update_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=parameters,
                Capabilities=['CAPABILITY_NAMED_IAM']
            )
            logger.info(f"Updating existing S3 stack {stack_name}")
        else:
            response = self.cloudformation_client.create_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=parameters,
                Capabilities=['CAPABILITY_NAMED_IAM']
            )
            logger.info(f"Creating new S3 stack {stack_name}")
        
        # Wait for stack to complete
        waiter = self.cloudformation_client.get_waiter('stack_create_complete' if not stack_exists else 'stack_update_complete')
        waiter.wait(StackName=stack_name)
        
        # Get stack outputs
        stack_response = self.cloudformation_client.describe_stacks(StackName=stack_name)
        outputs = {
            output['OutputKey']: output['OutputValue'] 
            for output in stack_response['Stacks'][0]['Outputs']
        }
        
        return {
            'stack_id': response['StackId'],
            'stack_name': stack_name,
            'outputs': outputs,
            'main_bucket': outputs.get('MainModelBucketName'),
            'client_bucket': outputs.get('ClientModelBucketName'),
            'encryption_key_arn': outputs.get('ModelEncryptionKeyArn'),
            'service_role_arn': outputs.get('ServiceRoleArn')
        }

    def create_ec2_resources(
        self,
        instance_type: str = "g4dn.xlarge",
        key_name: Optional[str] = None,
        vpc_id: Optional[str] = None,
        subnet_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create EC2 instance and related resources using CloudFormation.

        Args:
            instance_type: EC2 instance type
            key_name: EC2 key pair name for SSH access
            vpc_id: VPC ID for the resources
            subnet_id: Subnet ID for the EC2 instance

        Returns:
            Dictionary with stack outputs
        """
        logger.info(f"Creating EC2 resources for client {self.client_id}")
        
        # Get default VPC if not provided
        if not vpc_id:
            vpcs = self.ec2_client.describe_vpcs(Filters=[{'Name': 'isDefault', 'Values': ['true']}])
            if vpcs['Vpcs']:
                vpc_id = vpcs['Vpcs'][0]['VpcId']
                logger.info(f"Using default VPC: {vpc_id}")
            else:
                raise ValueError("No default VPC found and no VPC ID provided")
                
        # Get first subnet in VPC if not provided
        if not subnet_id:
            subnets = self.ec2_client.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
            if subnets['Subnets']:
                subnet_id = subnets['Subnets'][0]['SubnetId']
                logger.info(f"Using subnet: {subnet_id}")
            else:
                raise ValueError(f"No subnets found in VPC {vpc_id}")
        
        # Get latest Amazon Linux 2 AMI with GPU support
        ami_response = self.ec2_client.describe_images(
            Owners=['amazon'],
            Filters=[
                {'Name': 'name', 'Values': ['amzn2-ami-graphics-*']},
                {'Name': 'architecture', 'Values': ['x86_64']},
                {'Name': 'virtualization-type', 'Values': ['hvm']},
                {'Name': 'root-device-type', 'Values': ['ebs']},
                {'Name': 'state', 'Values': ['available']}
            ]
        )
        
        if not ami_response['Images']:
            # Fallback to standard Amazon Linux 2
            ami_response = self.ec2_client.describe_images(
                Owners=['amazon'],
                Filters=[
                    {'Name': 'name', 'Values': ['amzn2-ami-hvm-*-x86_64-gp2']},
                    {'Name': 'architecture', 'Values': ['x86_64']},
                    {'Name': 'virtualization-type', 'Values': ['hvm']},
                    {'Name': 'root-device-type', 'Values': ['ebs']},
                    {'Name': 'state', 'Values': ['available']}
                ]
            )
        
        ami_id = sorted(ami_response['Images'], key=lambda x: x['CreationDate'], reverse=True)[0]['ImageId']
        logger.info(f"Using AMI: {ami_id}")
        
        # Create EC2 stack
        template_path = os.path.join(self.config_dir, "ec2-template.yaml")
        with open(template_path, 'r') as f:
            template_body = f.read()
        
        stack_name = f"secure-model-service-ec2-{self.client_id}-{self.environment}"
        
        # If key_name is not provided, check if we have any existing key pairs
        if not key_name:
            key_pairs = self.ec2_client.describe_key_pairs()
            if key_pairs['KeyPairs']:
                key_name = key_pairs['KeyPairs'][0]['KeyName']
                logger.info(f"Using existing key pair: {key_name}")
            else:
                # Create a new key pair
                key_name = f"secure-model-service-{self.client_id}"
                logger.info(f"Creating new key pair: {key_name}")
                key_response = self.ec2_client.create_key_pair(KeyName=key_name)
                
                # Save private key to a file (in production this should be handled securely)
                with tempfile.NamedTemporaryFile(delete=False, mode='w') as f:
                    f.write(key_response['KeyMaterial'])
                    key_file = f.name
                    
                logger.info(f"Private key saved to {key_file}")
        
        # Check if stack already exists
        try:
            self.cloudformation_client.describe_stacks(StackName=stack_name)
            stack_exists = True
        except botocore.exceptions.ClientError:
            stack_exists = False
            
        # Create or update stack
        parameters = [
            {'ParameterKey': 'ClientId', 'ParameterValue': self.client_id},
            {'ParameterKey': 'Environment', 'ParameterValue': self.environment},
            {'ParameterKey': 'InstanceType', 'ParameterValue': instance_type},
            {'ParameterKey': 'KeyName', 'ParameterValue': key_name},
            {'ParameterKey': 'VpcId', 'ParameterValue': vpc_id},
            {'ParameterKey': 'SubnetId', 'ParameterValue': subnet_id},
            {'ParameterKey': 'ImageId', 'ParameterValue': ami_id}
        ]
        
        if stack_exists:
            response = self.cloudformation_client.update_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=parameters,
                Capabilities=['CAPABILITY_NAMED_IAM']
            )
            logger.info(f"Updating existing EC2 stack {stack_name}")
        else:
            response = self.cloudformation_client.create_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=parameters,
                Capabilities=['CAPABILITY_NAMED_IAM']
            )
            logger.info(f"Creating new EC2 stack {stack_name}")
        
        # Wait for stack to complete
        waiter = self.cloudformation_client.get_waiter('stack_create_complete' if not stack_exists else 'stack_update_complete')
        waiter.wait(StackName=stack_name)
        
        # Get stack outputs
        stack_response = self.cloudformation_client.describe_stacks(StackName=stack_name)
        outputs = {
            output['OutputKey']: output['OutputValue'] 
            for output in stack_response['Stacks'][0]['Outputs']
        }
        
        return {
            'stack_id': response['StackId'],
            'stack_name': stack_name,
            'outputs': outputs,
            'instance_id': outputs.get('InstanceId'),
            'public_ip': outputs.get('PublicIP'),
            'elastic_ip': outputs.get('ElasticIP'),
            'key_name': key_name
        }

    def create_lambda_resources(self, model_service_endpoint: str) -> Dict[str, Any]:
        """
        Create Lambda function and API Gateway for model endpoint.

        Args:
            model_service_endpoint: Endpoint for the model service

        Returns:
            Dictionary with stack outputs
        """
        logger.info(f"Creating Lambda resources for client {self.client_id}")
        
        template_path = os.path.join(self.config_dir, "lambda-template.yaml")
        with open(template_path, 'r') as f:
            template_body = f.read()
        
        stack_name = f"secure-model-service-lambda-{self.client_id}-{self.environment}"
        
        # Check if stack already exists
        try:
            self.cloudformation_client.describe_stacks(StackName=stack_name)
            stack_exists = True
        except botocore.exceptions.ClientError:
            stack_exists = False
            
        # Create or update stack
        parameters = [
            {'ParameterKey': 'ClientId', 'ParameterValue': self.client_id},
            {'ParameterKey': 'Environment', 'ParameterValue': self.environment},
            {'ParameterKey': 'ModelServiceEndpoint', 'ParameterValue': model_service_endpoint},
            {'ParameterKey': 'ApiStageName', 'ParameterValue': 'v1'}
        ]
        
        if stack_exists:
            response = self.cloudformation_client.update_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=parameters,
                Capabilities=['CAPABILITY_NAMED_IAM']
            )
            logger.info(f"Updating existing Lambda stack {stack_name}")
        else:
            response = self.cloudformation_client.create_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=parameters,
                Capabilities=['CAPABILITY_NAMED_IAM']
            )
            logger.info(f"Creating new Lambda stack {stack_name}")
        
        # Wait for stack to complete
        waiter = self.cloudformation_client.get_waiter('stack_create_complete' if not stack_exists else 'stack_update_complete')
        waiter.wait(StackName=stack_name)
        
        # Get stack outputs
        stack_response = self.cloudformation_client.describe_stacks(StackName=stack_name)
        outputs = {
            output['OutputKey']: output['OutputValue'] 
            for output in stack_response['Stacks'][0]['Outputs']
        }
        
        # Get API key value (this is a separate call as it's not included in stack outputs)
        api_key_id = outputs.get('ApiKeyId')
        api_key_response = self.session.client('apigateway').get_api_key(
            apiKey=api_key_id,
            includeValue=True
        )
        api_key_value = api_key_response.get('value')
        
        return {
            'stack_id': response['StackId'],
            'stack_name': stack_name,
            'outputs': outputs,
            'api_endpoint': outputs.get('ApiEndpoint'),
            'api_key_id': api_key_id,
            'api_key_value': api_key_value
        }

    def upload_model_to_s3(self, local_path: str, s3_key: Optional[str] = None) -> str:
        """
        Upload a model to S3.

        Args:
            local_path: Local path to the model file
            s3_key: S3 key to upload to (defaults to basename of local_path)

        Returns:
            S3 URI of the uploaded model
        """
        if not s3_key:
            s3_key = os.path.basename(local_path)
        
        # Add client prefix
        if not s3_key.startswith(f"clients/{self.client_id}/"):
            s3_key = f"clients/{self.client_id}/models/{s3_key}"
        
        logger.info(f"Uploading model from {local_path} to s3://{self.client_bucket}/{s3_key}")
        
        # Upload file with server-side encryption
        self.s3_client.upload_file(
            local_path,
            self.client_bucket,
            s3_key,
            ExtraArgs={'ServerSideEncryption': 'AES256'}
        )
        
        return f"s3://{self.client_bucket}/{s3_key}"

    def download_model_from_s3(self, s3_key: str, local_path: Optional[str] = None) -> str:
        """
        Download a model from S3.

        Args:
            s3_key: S3 key to download
            local_path: Local path to save to (defaults to basename of s3_key)

        Returns:
            Local path to the downloaded model
        """
        # Add client prefix if not present
        if not s3_key.startswith(f"clients/{self.client_id}/"):
            s3_key = f"clients/{self.client_id}/models/{s3_key}"
        
        if not local_path:
            local_path = os.path.basename(s3_key)
            
            # Create a temporary directory if local_path doesn't include a directory
            if os.path.dirname(local_path) == '':
                temp_dir = tempfile.mkdtemp()
                local_path = os.path.join(temp_dir, local_path)
        
        logger.info(f"Downloading model from s3://{self.client_bucket}/{s3_key} to {local_path}")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # Download file
        self.s3_client.download_file(
            self.client_bucket,
            s3_key,
            local_path
        )
        
        return local_path
