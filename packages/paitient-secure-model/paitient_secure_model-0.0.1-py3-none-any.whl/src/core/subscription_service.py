#!/usr/bin/env python3
"""
Subscription Service

This module handles subscription validation and implements automated lockout
for users who don't have an active subscription.
"""

import os
import json
import time
import logging
import threading
import requests
from typing import Dict, Optional, List, Any, Callable
from datetime import datetime, timedelta

# Configure logging
logger = logging.getLogger(__name__)

class SubscriptionCache:
    """In-memory cache for subscription status."""
    
    def __init__(self, cache_ttl_seconds: int = 300):
        """
        Initialize the subscription cache.
        
        Args:
            cache_ttl_seconds: Time-to-live for cache entries in seconds
        """
        self.cache = {}
        self.cache_ttl_seconds = cache_ttl_seconds
        self.lock = threading.Lock()
    
    def get(self, client_id: str) -> Optional[Dict[str, Any]]:
        """
        Get subscription status from cache.
        
        Args:
            client_id: Client identifier
            
        Returns:
            Cached subscription status or None if not in cache
        """
        with self.lock:
            if client_id not in self.cache:
                return None
            
            cache_entry = self.cache[client_id]
            if cache_entry["expires_at"] < datetime.now():
                # Cache entry has expired
                del self.cache[client_id]
                return None
            
            return cache_entry["data"]
    
    def set(self, client_id: str, data: Dict[str, Any]) -> None:
        """
        Store subscription status in cache.
        
        Args:
            client_id: Client identifier
            data: Subscription status data
        """
        with self.lock:
            expires_at = datetime.now() + timedelta(seconds=self.cache_ttl_seconds)
            self.cache[client_id] = {
                "data": data,
                "expires_at": expires_at
            }
    
    def invalidate(self, client_id: str) -> None:
        """
        Invalidate cache entry for client.
        
        Args:
            client_id: Client identifier
        """
        with self.lock:
            if client_id in self.cache:
                del self.cache[client_id]

class SubscriptionService:
    """Service for validating user subscriptions."""
    
    def __init__(
        self, 
        subscription_endpoint: str, 
        subscription_key: str, 
        check_frequency: int = 60,
        cache_ttl: int = 300
    ):
        """
        Initialize the subscription service.
        
        Args:
            subscription_endpoint: Endpoint for verifying subscriptions
            subscription_key: API key for subscription service
            check_frequency: How often to check subscription status (seconds)
            cache_ttl: Time-to-live for cache entries (seconds)
        """
        self.subscription_endpoint = subscription_endpoint
        self.subscription_key = subscription_key
        self.check_frequency = check_frequency
        self.cache = SubscriptionCache(cache_ttl_seconds=cache_ttl)
        self.active_clients = set()
        self.lock = threading.Lock()
        self.shutdown_flag = threading.Event()
        self.background_thread = None
    
    def start_background_checker(self) -> None:
        """Start background thread to periodically check subscription status."""
        if self.background_thread is not None:
            return
        
        self.shutdown_flag.clear()
        self.background_thread = threading.Thread(
            target=self._subscription_checker_thread,
            daemon=True
        )
        self.background_thread.start()
        logger.info("Started subscription checker background thread")
    
    def stop_background_checker(self) -> None:
        """Stop the background subscription checker thread."""
        if self.background_thread is None:
            return
        
        self.shutdown_flag.set()
        self.background_thread.join(timeout=10)
        self.background_thread = None
        logger.info("Stopped subscription checker background thread")
    
    def _subscription_checker_thread(self) -> None:
        """Background thread for checking subscription status."""
        while not self.shutdown_flag.is_set():
            try:
                with self.lock:
                    clients_to_check = list(self.active_clients)
                
                for client_id in clients_to_check:
                    self.check_subscription(client_id, force_remote=True)
            
            except Exception as e:
                logger.error(f"Error in subscription checker thread: {e}")
            
            # Sleep until next check cycle
            self.shutdown_flag.wait(timeout=self.check_frequency)
    
    def register_client(self, client_id: str) -> None:
        """
        Register a client for subscription monitoring.
        
        Args:
            client_id: Client identifier
        """
        with self.lock:
            self.active_clients.add(client_id)
        logger.info(f"Registered client {client_id} for subscription monitoring")
    
    def unregister_client(self, client_id: str) -> None:
        """
        Unregister a client from subscription monitoring.
        
        Args:
            client_id: Client identifier
        """
        with self.lock:
            self.active_clients.discard(client_id)
        self.cache.invalidate(client_id)
        logger.info(f"Unregistered client {client_id} from subscription monitoring")
    
    def check_subscription(
        self, 
        client_id: str, 
        api_key: Optional[str] = None,
        force_remote: bool = False
    ) -> Dict[str, Any]:
        """
        Check subscription status for a client.
        
        Args:
            client_id: Client identifier
            api_key: Client's API key (optional)
            force_remote: If True, bypass cache and check with remote service
            
        Returns:
            Subscription status information
            
        Raises:
            SubscriptionError: If subscription check fails
        """
        # Check cache first (unless forcing remote check)
        if not force_remote:
            cached_status = self.cache.get(client_id)
            if cached_status is not None:
                return cached_status
        
        # Prepare request to subscription endpoint
        headers = {
            "Content-Type": "application/json",
            "X-Subscription-Key": self.subscription_key
        }
        
        data = {
            "client_id": client_id
        }
        
        if api_key:
            data["api_key"] = api_key
        
        try:
            response = requests.post(
                self.subscription_endpoint,
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code != 200:
                error_msg = f"Subscription check failed with status {response.status_code}"
                logger.error(f"{error_msg}: {response.text}")
                raise SubscriptionError(error_msg)
            
            subscription_data = response.json()
            
            # Cache the result
            self.cache.set(client_id, subscription_data)
            
            # Register client for background checking if active
            if subscription_data.get("is_active", False):
                self.register_client(client_id)
            else:
                self.unregister_client(client_id)
            
            return subscription_data
            
        except requests.RequestException as e:
            logger.error(f"Error checking subscription for client {client_id}: {e}")
            raise SubscriptionError(f"Subscription check failed: {e}")
    
    def validate_subscription(self, client_id: str, api_key: Optional[str] = None) -> bool:
        """
        Validate if a client has an active subscription.
        
        Args:
            client_id: Client identifier
            api_key: Client's API key (optional)
            
        Returns:
            True if subscription is active, False otherwise
        """
        try:
            subscription_data = self.check_subscription(client_id, api_key)
            is_active = subscription_data.get("is_active", False)
            
            if is_active:
                logger.info(f"Subscription is active for client {client_id}")
            else:
                logger.warning(f"Subscription is NOT active for client {client_id}")
            
            return is_active
        except SubscriptionError:
            # Default to inactive if check fails
            return False

class SubscriptionError(Exception):
    """Exception raised for subscription validation errors."""
    pass

# Singleton instance
_subscription_service = None

def get_subscription_service() -> SubscriptionService:
    """
    Get or create the subscription service singleton.
    
    Returns:
        SubscriptionService instance
    """
    global _subscription_service
    
    if _subscription_service is None:
        # Get config from environment
        subscription_endpoint = os.environ.get(
            "SUBSCRIPTION_CHECK_ENDPOINT",
            "https://api.yourservice.com/v1/subscription/verify"
        )
        subscription_key = os.environ.get("SUBSCRIPTION_KEY", "")
        check_frequency = int(os.environ.get("SUBSCRIPTION_CHECK_FREQUENCY", "60"))
        
        _subscription_service = SubscriptionService(
            subscription_endpoint=subscription_endpoint,
            subscription_key=subscription_key,
            check_frequency=check_frequency
        )
        
        # Start background checker
        _subscription_service.start_background_checker()
    
    return _subscription_service
