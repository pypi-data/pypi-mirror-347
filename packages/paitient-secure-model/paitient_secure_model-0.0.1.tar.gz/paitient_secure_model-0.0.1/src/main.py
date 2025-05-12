"""
Main entry point for the Secure Model Service application.

This module initializes and runs the application, setting up logging,
environment variables, and the API server.
"""

import os
import sys
import logging
import argparse
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

from src.api.api_service import get_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Secure Model Service')
    
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='Host to bind the server to'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Port to bind the server to'
    )
    
    parser.add_argument(
        '--env',
        type=str,
        default='.env',
        help='Path to .env file'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    return parser.parse_args()


def load_env(env_file='.env'):
    """Load environment variables from .env file."""
    env_path = Path(env_file)
    
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        logger.info(f"Loaded environment variables from {env_path}")
    else:
        logger.warning(f"Environment file {env_path} not found, using system environment variables")
    
    # Set default environment variables if not set
    if not os.environ.get('AWS_REGION'):
        os.environ['AWS_REGION'] = 'us-west-2'
        logger.info("AWS_REGION not set, defaulting to us-west-2")
    
    # Check for required environment variables
    required_vars = [
        'MODEL_NAME',  # Default model name to use
    ]
    
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.warning(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.warning("Using default values for missing environment variables")
        
        # Set defaults for required variables
        if 'MODEL_NAME' in missing_vars:
            os.environ['MODEL_NAME'] = 'ZimaBlueAI/HuatuoGPT-o1-8B'
            logger.info("MODEL_NAME not set, defaulting to ZimaBlueAI/HuatuoGPT-o1-8B")


def main():
    """Run the application."""
    args = parse_args()
    
    # Load environment variables
    load_env(args.env)
    
    # Set log level
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.getLogger().setLevel(log_level)
    
    # Get FastAPI app
    app = get_app()
    
    # Run the server
    logger.info(f"Starting server on {args.host}:{args.port}")
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_level='debug' if args.debug else 'info'
    )


if __name__ == '__main__':
    main()
