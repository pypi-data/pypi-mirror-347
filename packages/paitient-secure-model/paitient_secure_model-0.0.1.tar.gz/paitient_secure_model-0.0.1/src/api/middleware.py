#!/usr/bin/env python3
"""
API Middleware

This module contains FastAPI middleware components for authentication,
subscription validation, and monitoring/logging.
"""

import time
import json
import logging
from typing import Dict, Callable, Optional

from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram, Gauge

from ..core.subscription_service import get_subscription_service, SubscriptionError

# Configure logging
logger = logging.getLogger(__name__)

# Prometheus metrics
API_REQUESTS = Counter(
    "api_requests_total", 
    "Total number of API requests received",
    ["endpoint", "method", "client_id"]
)
API_RESPONSES = Counter(
    "api_responses_total", 
    "Total number of API responses sent",
    ["endpoint", "method", "status_code", "client_id"]
)
REQUEST_DURATION = Histogram(
    "request_duration_seconds",
    "Request duration in seconds",
    ["endpoint", "method", "client_id"]
)
ACTIVE_REQUESTS = Gauge(
    "active_requests",
    "Number of active requests",
    ["client_id"]
)
SUBSCRIPTION_STATUS = Gauge(
    "subscription_status",
    "Subscription status (1=active, 0=inactive)",
    ["client_id"]
)

class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Middleware for API key authentication."""
    
    def __init__(
        self, 
        app, 
        api_key_header: str = "X-API-Key",
        api_key_query: str = "api_key",
        api_keys: Dict[str, str] = None,
        excluded_paths: list = None
    ):
        """
        Initialize the authentication middleware.
        
        Args:
            app: FastAPI application
            api_key_header: HTTP header name for API key
            api_key_query: Query parameter name for API key
            api_keys: Dictionary mapping API keys to client IDs
            excluded_paths: List of URL paths excluded from authentication
        """
        super().__init__(app)
        self.api_key_header = api_key_header
        self.api_key_query = api_key_query
        self.api_keys = api_keys or {}
        self.excluded_paths = excluded_paths or ["/api/v1/health", "/api/v1/ready", "/metrics"]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request for authentication.
        
        Args:
            request: FastAPI request
            call_next: Next middleware in chain
            
        Returns:
            Response from API or error response
        """
        # Skip authentication for excluded paths
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)
        
        # Get API key from header or query parameter
        api_key = request.headers.get(self.api_key_header)
        if not api_key and self.api_key_query:
            api_key = request.query_params.get(self.api_key_query)
        
        # Check authorization header
        if not api_key and "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                api_key = auth_header[7:]  # Remove "Bearer " prefix
        
        # Validate API key
        if not api_key or api_key not in self.api_keys:
            logger.warning(f"Invalid API key: {api_key} for {request.url.path}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status": "error",
                    "message": "Invalid or missing API key"
                }
            )
        
        # Add client ID to request state
        client_id = self.api_keys.get(api_key)
        request.state.client_id = client_id
        request.state.api_key = api_key
        
        # Continue to next middleware
        return await call_next(request)

class SubscriptionMiddleware(BaseHTTPMiddleware):
    """Middleware for subscription validation."""
    
    def __init__(
        self, 
        app, 
        excluded_paths: list = None
    ):
        """
        Initialize the subscription middleware.
        
        Args:
            app: FastAPI application
            excluded_paths: List of URL paths excluded from subscription checks
        """
        super().__init__(app)
        self.excluded_paths = excluded_paths or ["/api/v1/health", "/api/v1/ready", "/metrics"]
        self.subscription_service = get_subscription_service()
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request for subscription validation.
        
        Args:
            request: FastAPI request
            call_next: Next middleware in chain
            
        Returns:
            Response from API or error response
        """
        # Skip subscription checks for excluded paths
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)
        
        # Get client ID from request state (set by AuthenticationMiddleware)
        client_id = getattr(request.state, "client_id", None)
        api_key = getattr(request.state, "api_key", None)
        
        if not client_id:
            logger.error("Client ID not found in request state")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "status": "error",
                    "message": "Internal server error"
                }
            )
        
        # Check subscription status
        try:
            has_active_subscription = self.subscription_service.validate_subscription(
                client_id=client_id,
                api_key=api_key
            )
            
            # Update Prometheus gauge
            SUBSCRIPTION_STATUS.labels(client_id=client_id).set(1 if has_active_subscription else 0)
            
            if not has_active_subscription:
                logger.warning(f"Subscription inactive for client {client_id}")
                return JSONResponse(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    content={
                        "status": "error",
                        "message": "Subscription inactive or expired",
                        "code": "subscription_required"
                    }
                )
                
        except SubscriptionError as e:
            logger.error(f"Subscription check failed for client {client_id}: {e}")
            # Continue processing if subscription check fails
            # This prevents service disruption but logs the error
        
        # Continue to next middleware
        return await call_next(request)

class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware for API metrics collection."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and collect metrics.
        
        Args:
            request: FastAPI request
            call_next: Next middleware in chain
            
        Returns:
            Response from API
        """
        # Get client ID from request state or use "anonymous"
        client_id = getattr(request.state, "client_id", "anonymous")
        
        # Extract endpoint and method
        endpoint = request.url.path
        method = request.method
        
        # Increment request counter
        API_REQUESTS.labels(endpoint=endpoint, method=method, client_id=client_id).inc()
        
        # Track active requests
        ACTIVE_REQUESTS.labels(client_id=client_id).inc()
        
        # Measure request duration
        start_time = time.time()
        
        try:
            # Process request
            response = await call_next(request)
            
            # Record metrics
            duration = time.time() - start_time
            REQUEST_DURATION.labels(
                endpoint=endpoint, 
                method=method,
                client_id=client_id
            ).observe(duration)
            
            API_RESPONSES.labels(
                endpoint=endpoint,
                method=method,
                status_code=response.status_code,
                client_id=client_id
            ).inc()
            
            return response
            
        except Exception as e:
            # Record exception metrics
            API_RESPONSES.labels(
                endpoint=endpoint,
                method=method,
                status_code=500,
                client_id=client_id
            ).inc()
            
            logger.exception(f"Exception during request processing: {e}")
            raise
        
        finally:
            # Decrement active requests counter
            ACTIVE_REQUESTS.labels(client_id=client_id).dec()

class AuditLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for HIPAA/SOC2 compliant audit logging."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and create audit logs.
        
        Args:
            request: FastAPI request
            call_next: Next middleware in chain
            
        Returns:
            Response from API
        """
        # Get client ID from request state or use "anonymous"
        client_id = getattr(request.state, "client_id", "anonymous")
        
        # Create request audit log
        audit_logger = logging.getLogger("audit")
        
        # Capture key request details for audit
        request_details = {
            "timestamp": time.time(),
            "client_id": client_id,
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "remote_addr": request.client.host if request.client else None,
            "user_agent": request.headers.get("User-Agent"),
            "request_id": request.headers.get("X-Request-ID", "")
        }
        
        # Log request with structured data
        audit_logger.info(
            f"API Request: {request.method} {request.url.path}",
            extra={"client_id": client_id, "audit_data": request_details}
        )
        
        # Process request
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        
        # Create response audit log
        response_details = {
            "timestamp": time.time(),
            "client_id": client_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration": duration,
            "request_id": request.headers.get("X-Request-ID", "")
        }
        
        # Log response with structured data
        audit_logger.info(
            f"API Response: {response.status_code} for {request.method} {request.url.path}",
            extra={"client_id": client_id, "audit_data": response_details}
        )
        
        return response
