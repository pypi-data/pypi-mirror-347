"""
Configuration Service for Secure Model Service

This module provides functionality for loading and managing configuration 
from environment variables, files, and other sources.
"""

import os
import logging
import json
from pathlib import Path
from typing import Dict, Any, Optional, Union

import yaml
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class ConfigService:
    """Service for managing application configuration."""

    def __init__(
        self,
        env_file: Optional[str] = None,
        config_dir: Optional[str] = None,
        environment: Optional[str] = None
    ):
        """
        Initialize the configuration service.

        Args:
            env_file: Path to .env file
            config_dir: Directory containing configuration files
            environment: Environment name (dev, staging, prod)
        """
        self.config = {}
        
        # Load environment variables from .env file if provided
        if env_file and os.path.exists(env_file):
            logger.info(f"Loading environment variables from {env_file}")
            load_dotenv(dotenv_path=env_file)
            
        # Set environment (from env var or parameter)
        self.environment = environment or os.environ.get("ENVIRONMENT", "dev")
        
        # Determine config directory
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            # Default to 'config' directory in project root
            self.config_dir = Path(__file__).parent.parent.parent / "config"
            
        logger.info(f"Config directory: {self.config_dir}")
        logger.info(f"Environment: {self.environment}")
            
        # Load configuration
        self._load_config()
    
    def _load_config(self):
        """Load configuration from files and environment variables."""
        # Load base config
        base_config_path = self.config_dir / "base_config.yaml"
        if base_config_path.exists():
            self._load_config_file(base_config_path)
        
        # Load environment-specific config
        env_config_path = self.config_dir / f"{self.environment}_config.yaml"
        if env_config_path.exists():
            self._load_config_file(env_config_path)
            
        # Override with environment variables
        self._load_from_env_vars()
        
        logger.debug(f"Loaded configuration: {self.config}")
    
    def _load_config_file(self, config_path: Union[str, Path]):
        """Load configuration from a YAML file."""
        logger.info(f"Loading configuration from {config_path}")
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                if config:
                    self._merge_config(config)
        except Exception as e:
            logger.error(f"Error loading config from {config_path}: {str(e)}")
    
    def _load_from_env_vars(self):
        """Load configuration from environment variables."""
        # Look for environment variables with the prefix CONFIG_
        for key, value in os.environ.items():
            if key.startswith("CONFIG_"):
                # Convert CONFIG_SECTION_KEY to section.key
                config_key = key[7:].lower().replace("_", ".")
                self.set(config_key, value)
    
    def _merge_config(self, config: Dict[str, Any], prefix: str = ""):
        """
        Merge configuration dictionary into the current config.
        
        Args:
            config: Configuration dictionary to merge
            prefix: Key prefix for nested dictionaries
        """
        for key, value in config.items():
            full_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                # Recursively merge nested dictionaries
                self._merge_config(value, full_key)
            else:
                # Set the value
                self.set(full_key, value)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key (dot-separated for nested keys)
            default: Default value if key is not found
            
        Returns:
            Configuration value
        """
        # Split the key by dots
        keys = key.split(".")
        
        # Traverse the config dictionary
        current = self.config
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        
        return current
    
    def set(self, key: str, value: Any):
        """
        Set a configuration value.
        
        Args:
            key: Configuration key (dot-separated for nested keys)
            value: Value to set
        """
        # Split the key by dots
        keys = key.split(".")
        
        # Traverse the config dictionary and create intermediate dictionaries as needed
        current = self.config
        for i, k in enumerate(keys[:-1]):
            if k not in current:
                current[k] = {}
            elif not isinstance(current[k], dict):
                # If the current value is not a dict, convert it to a dict
                current[k] = {}
            current = current[k]
        
        # Set the value
        current[keys[-1]] = value
    
    def save(self, config_path: Optional[Union[str, Path]] = None):
        """
        Save the current configuration to a file.
        
        Args:
            config_path: Path to save the configuration to
        """
        if not config_path:
            config_path = self.config_dir / f"{self.environment}_config.yaml"
            
        logger.info(f"Saving configuration to {config_path}")
        try:
            with open(config_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
        except Exception as e:
            logger.error(f"Error saving config to {config_path}: {str(e)}")
            raise
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Get the configuration as a dictionary.
        
        Returns:
            Configuration dictionary
        """
        return self.config.copy()


# Singleton instance
_config_service = None


def get_config_service(
    env_file: Optional[str] = None, 
    config_dir: Optional[str] = None,
    environment: Optional[str] = None
) -> ConfigService:
    """
    Get the singleton config service instance.
    
    Args:
        env_file: Path to .env file
        config_dir: Directory containing configuration files
        environment: Environment name (dev, staging, prod)
        
    Returns:
        Config service instance
    """
    global _config_service
    if _config_service is None:
        _config_service = ConfigService(env_file, config_dir, environment)
    return _config_service
