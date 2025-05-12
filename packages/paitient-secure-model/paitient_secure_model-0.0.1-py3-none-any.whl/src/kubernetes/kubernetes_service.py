"""
Kubernetes Service Module for Secure Model Service

This module provides functionality to create and manage Kubernetes resources
for deploying secure model endpoints.
"""

import os
import logging
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List

import yaml
from kubernetes import client, config
from jinja2 import Template

logger = logging.getLogger(__name__)


class KubernetesService:
    """Service for managing Kubernetes resources for model deployments."""

    def __init__(
        self,
        namespace: str = "default",
        config_dir: str = "/app/config/kubernetes",
        kubeconfig_path: Optional[str] = None,
    ):
        """
        Initialize the Kubernetes service.

        Args:
            namespace: Kubernetes namespace to deploy resources to
            config_dir: Directory containing Kubernetes template files
            kubeconfig_path: Path to kubeconfig file
        """
        self.namespace = namespace
        self.config_dir = Path(config_dir)
        
        # Load Kubernetes configuration
        if kubeconfig_path:
            config.load_kube_config(config_file=kubeconfig_path)
        else:
            try:
                config.load_incluster_config()
            except config.config_exception.ConfigException:
                # Fallback to kubeconfig
                config.load_kube_config()
        
        # Initialize Kubernetes clients
        self.core_api = client.CoreV1Api()
        self.apps_api = client.AppsV1Api()
        self.custom_api = client.CustomObjectsApi()
        self.autoscaling_api = client.AutoscalingV1Api()
        
    def _render_template(self, template_path: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Render a Kubernetes YAML template using provided context variables.

        Args:
            template_path: Path to the template file
            context: Dictionary of context variables for template rendering

        Returns:
            Rendered YAML as dictionary
        """
        with open(template_path, 'r') as f:
            template_content = f.read()
            
        template = Template(template_content)
        rendered_yaml = template.render(**context)
        
        return yaml.safe_load(rendered_yaml)

    def _apply_kubernetes_object(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply a Kubernetes object configuration.

        Args:
            obj: Kubernetes object configuration as dictionary

        Returns:
            Created/updated Kubernetes object
        """
        kind = obj.get("kind")
        api_version = obj.get("apiVersion")
        metadata = obj.get("metadata", {})
        name = metadata.get("name")
        namespace = metadata.get("namespace", self.namespace)
        
        logger.info(f"Applying {kind} {namespace}/{name}")
        
        # Different handling based on object kind
        if kind == "Deployment":
            return self.apps_api.create_namespaced_deployment(
                namespace=namespace,
                body=obj
            )
        elif kind == "Service":
            return self.core_api.create_namespaced_service(
                namespace=namespace,
                body=obj
            )
        elif kind == "PersistentVolumeClaim":
            return self.core_api.create_namespaced_persistent_volume_claim(
                namespace=namespace,
                body=obj
            )
        elif kind == "ConfigMap":
            return self.core_api.create_namespaced_config_map(
                namespace=namespace,
                body=obj
            )
        elif kind == "Secret":
            return self.core_api.create_namespaced_secret(
                namespace=namespace,
                body=obj
            )
        elif kind == "HorizontalPodAutoscaler":
            return self.autoscaling_api.create_namespaced_horizontal_pod_autoscaler(
                namespace=namespace,
                body=obj
            )
        else:
            raise ValueError(f"Unsupported Kubernetes object kind: {kind}")

    def create_namespace(self, namespace: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a Kubernetes namespace if it doesn't exist.

        Args:
            namespace: Name of the namespace to create, defaults to the initialized namespace

        Returns:
            Created namespace object
        """
        if not namespace:
            namespace = self.namespace
        
        # Check if namespace already exists
        try:
            self.core_api.read_namespace(name=namespace)
            logger.info(f"Namespace {namespace} already exists")
            return {"name": namespace, "status": "exists"}
        except client.exceptions.ApiException as e:
            if e.status == 404:
                # Create namespace
                ns_manifest = {
                    "apiVersion": "v1",
                    "kind": "Namespace",
                    "metadata": {
                        "name": namespace,
                        "labels": {
                            "name": namespace
                        }
                    }
                }
                
                self.core_api.create_namespace(body=ns_manifest)
                logger.info(f"Created namespace {namespace}")
                return {"name": namespace, "status": "created"}
            else:
                logger.error(f"Failed to check/create namespace {namespace}: {e}")
                raise

    def deploy_model_service(
        self,
        client_id: str,
        model_name: str,
        image_uri: str,
        gpu_count: int = 1,
        cpu_limit: str = "4",
        memory_limit: str = "16Gi",
        s3_bucket: Optional[str] = None,
        encryption_key_arn: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Deploy a model service for a client.

        Args:
            client_id: Unique identifier for the client
            model_name: Name of the model to deploy
            image_uri: URI of the Docker image
            gpu_count: Number of GPUs to allocate
            cpu_limit: CPU limit for the deployment
            memory_limit: Memory limit for the deployment
            s3_bucket: S3 bucket for model storage
            encryption_key_arn: ARN of the KMS key for encryption

        Returns:
            Dictionary with deployment details
        """
        # Create namespace for client
        namespace = f"client-{client_id}"
        self.create_namespace(namespace)
        
        # Define context for templates
        context = {
            "CLIENT_ID": client_id,
            "CLIENT_NAMESPACE": namespace,
            "MODEL_NAME": model_name,
            "ECR_REPOSITORY_URI": image_uri,
            "IMAGE_TAG": "latest",
            "GPU_COUNT": str(gpu_count),
            "S3_BUCKET": s3_bucket or "",
            "ENCRYPTION_KEY_ARN": encryption_key_arn or ""
        }
        
        # Create the necessary Kubernetes resources
        resources = {}
        
        # Create PVC
        pvc_template = self.config_dir / "pvc.yaml"
        pvc_obj = self._render_template(str(pvc_template), context)
        resources["pvc"] = self._apply_kubernetes_object(pvc_obj)
        
        # Create encryption key Secret if needed
        if encryption_key_arn:
            secret = {
                "apiVersion": "v1",
                "kind": "Secret",
                "metadata": {
                    "name": f"{client_id}-encryption-keys",
                    "namespace": namespace,
                    "labels": {
                        "app": "model-service",
                        "client": client_id
                    }
                },
                "stringData": {
                    "encryption_key_arn": encryption_key_arn
                }
            }
            resources["secret"] = self._apply_kubernetes_object(secret)
        
        # Create Deployment
        deployment_template = self.config_dir / "deployment.yaml"
        deployment_obj = self._render_template(str(deployment_template), context)
        resources["deployment"] = self._apply_kubernetes_object(deployment_obj)
        
        # Create Service
        service_template = self.config_dir / "service.yaml"
        service_obj = self._render_template(str(service_template), context)
        resources["service"] = self._apply_kubernetes_object(service_obj)
        
        # Create HorizontalPodAutoscaler
        hpa = {
            "apiVersion": "autoscaling/v1",
            "kind": "HorizontalPodAutoscaler",
            "metadata": {
                "name": f"{client_id}-model-service-hpa",
                "namespace": namespace,
                "labels": {
                    "app": "model-service",
                    "client": client_id
                }
            },
            "spec": {
                "scaleTargetRef": {
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "name": f"{client_id}-model-service"
                },
                "minReplicas": 1,
                "maxReplicas": 3,
                "targetCPUUtilizationPercentage": 80
            }
        }
        resources["hpa"] = self._apply_kubernetes_object(hpa)
        
        logger.info(f"Successfully deployed model service for client {client_id}")
        
        return {
            "namespace": namespace,
            "deployment_name": f"{client_id}-model-service",
            "service_name": f"{client_id}-model-service",
            "endpoint": f"{client_id}-model-service.{namespace}.svc.cluster.local"
        }

    def delete_model_service(self, client_id: str) -> Dict[str, Any]:
        """
        Delete a model service deployment.

        Args:
            client_id: Unique identifier for the client

        Returns:
            Status of deletion
        """
        namespace = f"client-{client_id}"
        
        # Delete Deployment
        try:
            self.apps_api.delete_namespaced_deployment(
                name=f"{client_id}-model-service",
                namespace=namespace
            )
            logger.info(f"Deleted deployment {client_id}-model-service")
        except client.exceptions.ApiException as e:
            if e.status != 404:  # Ignore if not found
                logger.error(f"Failed to delete deployment: {e}")
                raise
        
        # Delete Service
        try:
            self.core_api.delete_namespaced_service(
                name=f"{client_id}-model-service",
                namespace=namespace
            )
            logger.info(f"Deleted service {client_id}-model-service")
        except client.exceptions.ApiException as e:
            if e.status != 404:  # Ignore if not found
                logger.error(f"Failed to delete service: {e}")
                raise
        
        # Delete PVC
        try:
            self.core_api.delete_namespaced_persistent_volume_claim(
                name=f"{client_id}-model-pvc",
                namespace=namespace
            )
            logger.info(f"Deleted PVC {client_id}-model-pvc")
        except client.exceptions.ApiException as e:
            if e.status != 404:  # Ignore if not found
                logger.error(f"Failed to delete PVC: {e}")
                raise
        
        # Delete Secret
        try:
            self.core_api.delete_namespaced_secret(
                name=f"{client_id}-encryption-keys",
                namespace=namespace
            )
            logger.info(f"Deleted secret {client_id}-encryption-keys")
        except client.exceptions.ApiException as e:
            if e.status != 404:  # Ignore if not found
                logger.error(f"Failed to delete secret: {e}")
                raise
        
        # Delete HorizontalPodAutoscaler
        try:
            self.autoscaling_api.delete_namespaced_horizontal_pod_autoscaler(
                name=f"{client_id}-model-service-hpa",
                namespace=namespace
            )
            logger.info(f"Deleted HPA {client_id}-model-service-hpa")
        except client.exceptions.ApiException as e:
            if e.status != 404:  # Ignore if not found
                logger.error(f"Failed to delete HPA: {e}")
                raise
        
        return {
            "status": "success",
            "message": f"Successfully deleted model service for client {client_id}"
        }

    def get_service_status(self, client_id: str) -> Dict[str, Any]:
        """
        Get status of a deployed model service.

        Args:
            client_id: Unique identifier for the client

        Returns:
            Status of the service deployment
        """
        namespace = f"client-{client_id}"
        
        try:
            # Get Deployment status
            deployment = self.apps_api.read_namespaced_deployment_status(
                name=f"{client_id}-model-service",
                namespace=namespace
            )
            
            # Get Service details
            service = self.core_api.read_namespaced_service(
                name=f"{client_id}-model-service",
                namespace=namespace
            )
            
            # Get Pod details
            pod_list = self.core_api.list_namespaced_pod(
                namespace=namespace,
                label_selector=f"app=model-service,client={client_id}"
            )
            
            pods = []
            for pod in pod_list.items:
                pod_status = {
                    "name": pod.metadata.name,
                    "phase": pod.status.phase,
                    "host_ip": pod.status.host_ip,
                    "pod_ip": pod.status.pod_ip,
                    "conditions": [
                        {"type": c.type, "status": c.status}
                        for c in (pod.status.conditions or [])
                    ]
                }
                pods.append(pod_status)
            
            return {
                "status": "found",
                "deployment": {
                    "name": deployment.metadata.name,
                    "ready_replicas": deployment.status.ready_replicas or 0,
                    "replicas": deployment.status.replicas,
                    "available_replicas": deployment.status.available_replicas or 0,
                    "conditions": [
                        {"type": c.type, "status": c.status, "message": c.message}
                        for c in (deployment.status.conditions or [])
                    ]
                },
                "service": {
                    "name": service.metadata.name,
                    "type": service.spec.type,
                    "cluster_ip": service.spec.cluster_ip,
                    "ports": [
                        {"name": p.name, "port": p.port, "target_port": p.target_port}
                        for p in service.spec.ports
                    ]
                },
                "pods": pods,
                "endpoint": f"{client_id}-model-service.{namespace}.svc.cluster.local"
            }
        except client.exceptions.ApiException as e:
            if e.status == 404:
                return {
                    "status": "not_found",
                    "message": f"Service for client {client_id} not found"
                }
            else:
                logger.error(f"Failed to get service status: {e}")
                return {
                    "status": "error",
                    "message": str(e)
                }
