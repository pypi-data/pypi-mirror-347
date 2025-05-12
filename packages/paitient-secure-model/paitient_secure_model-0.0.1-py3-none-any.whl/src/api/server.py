#!/usr/bin/env python3
"""
Model Service API Server

This module implements the FastAPI server for the secure model service with
subscription validation, monitoring, and HIPAA/SOC2 compliant logging.
"""

import os
import json
import time
import logging
import asyncio
from typing import Dict, List, Optional, Any

import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from prometheus_client import make_asgi_app

from ..core.subscription_service import get_subscription_service
from ..core.config_service import load_config
from ..models.model_service import ModelService
from .middleware import (
    AuthenticationMiddleware, 
    SubscriptionMiddleware, 
    MetricsMiddleware,
    AuditLoggingMiddleware
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API models
class GenerateRequest(BaseModel):
    """Request model for text generation."""
    prompt: str = Field(..., description="Input prompt for generation")
    max_tokens: int = Field(256, description="Maximum number of tokens to generate")
    temperature: float = Field(0.7, description="Sampling temperature (0.0-1.0)")
    top_p: float = Field(0.9, description="Nucleus sampling parameter (0.0-1.0)")
    top_k: int = Field(50, description="Top-k sampling parameter")
    stop_sequences: Optional[List[str]] = Field(None, description="Sequences that stop generation")
    repetition_penalty: Optional[float] = Field(1.0, description="Repetition penalty")
    streaming: bool = Field(False, description="Whether to stream the response")

class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Service status")
    model_info: Dict[str, Any] = Field(..., description="Model information")

class GenerateResponse(BaseModel):
    """Response model for text generation."""
    text: str = Field(..., description="Generated text")
    usage: Dict[str, int] = Field(..., description="Token usage statistics")
    finish_reason: Optional[str] = Field(None, description="Reason for generation completion")

def create_app():
    """Create and configure the FastAPI application."""
    # Create FastAPI app
    app = FastAPI(
        title="Secure Model Service API",
        description="HIPAA/SOC2 compliant API for secure model hosting",
        version="1.0.0",
    )
    
    # Load configuration
    config = load_config()
    
    # Initialize model service
    model_service = ModelService(config)
    
    # Configure API keys and client IDs
    api_keys = {}
    api_key = os.environ.get("API_KEY", "")
    client_id = os.environ.get("CLIENT_ID", "")
    
    if api_key and client_id:
        api_keys[api_key] = client_id
    
    # Add middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add custom middleware (order matters)
    app.add_middleware(MetricsMiddleware)
    app.add_middleware(AuditLoggingMiddleware)
    app.add_middleware(AuthenticationMiddleware, api_keys=api_keys)
    app.add_middleware(SubscriptionMiddleware)
    
    # Mount Prometheus metrics
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)
    
    @app.get("/api/v1/health", response_model=HealthResponse)
    async def health_check():
        """Check service health."""
        # Get model status from model service
        model_info = model_service.get_status()
        
        return {
            "status": "online",
            "model_info": model_info
        }
    
    @app.get("/api/v1/ready")
    async def readiness_check():
        """Check if the service is ready to accept requests."""
        if not model_service.is_ready():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service not ready"
            )
        
        return {"status": "ready"}
    
    @app.post("/api/v1/generate", response_model=GenerateResponse)
    async def generate(request: Request, req: GenerateRequest):
        """
        Generate text from prompt.
        
        This endpoint requires an authenticated user with an active subscription.
        """
        client_id = request.state.client_id
        
        try:
            # Log prompt (redacted for sensitive data)
            redacted_prompt = req.prompt[:20] + "..." if len(req.prompt) > 20 else req.prompt
            logger.info(f"Generate request from client {client_id} with prompt: {redacted_prompt}")
            
            # Call model service to generate text
            start_time = time.time()
            result = await model_service.generate(
                client_id=client_id,
                prompt=req.prompt,
                max_tokens=req.max_tokens,
                temperature=req.temperature,
                top_p=req.top_p,
                top_k=req.top_k,
                stop_sequences=req.stop_sequences,
                repetition_penalty=req.repetition_penalty
            )
            duration = time.time() - start_time
            
            # Log generation details (without exposing generated text)
            logger.info(f"Generated {result['usage']['completion_tokens']} tokens in {duration:.2f}s for client {client_id}")
            
            return result
            
        except Exception as e:
            logger.exception(f"Error generating text: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating text: {str(e)}"
            )
    
    @app.get("/api/v1/status")
    async def subscription_status(request: Request):
        """Check subscription status for the authenticated client."""
        client_id = request.state.client_id
        api_key = request.state.api_key
        
        try:
            # Get subscription service
            subscription_service = get_subscription_service()
            
            # Check subscription status
            subscription_data = subscription_service.check_subscription(
                client_id=client_id,
                api_key=api_key
            )
            
            return subscription_data
            
        except Exception as e:
            logger.exception(f"Error checking subscription status: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error checking subscription status: {str(e)}"
            )
    
    return app

def start_server(host="0.0.0.0", port=8000, reload=False, debug=False):
    """Start the FastAPI server."""
    # Configure logging
    log_level = "debug" if debug else "info"
    
    # Start server
    app = create_app()
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level=log_level,
        reload=reload
    )

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Start the model service API server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload on code changes")
    
    args = parser.parse_args()
    
    start_server(
        host=args.host,
        port=args.port,
        reload=args.reload,
        debug=args.debug
    )
