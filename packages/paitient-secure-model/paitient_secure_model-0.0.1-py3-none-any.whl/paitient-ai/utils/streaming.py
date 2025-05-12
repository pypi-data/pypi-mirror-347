#!/usr/bin/env python3
"""
Streaming utilities for the Secure Model Service.
"""

import json
import logging
from typing import Dict, Any, Iterator, Optional

logger = logging.getLogger(__name__)

class GenerationStream:
    """
    Stream handler for text generation responses.
    
    This class provides an iterator interface for streaming responses
    from the model generation API.
    """
    
    def __init__(self, session, url: str, payload: Dict[str, Any]):
        """
        Initialize the generation stream.
        
        Args:
            session: Requests session
            url: API URL
            payload: Request payload
        """
        self.session = session
        self.url = url
        self.payload = payload
        self.response = None
        self._iterator = None
    
    def __iter__(self) -> 'GenerationStream':
        """
        Initialize the iterator.
        
        Returns:
            Self for iteration
        """
        # Ensure streaming is enabled
        payload = dict(self.payload)
        payload["streaming"] = True
        
        # Initialize the streaming request
        self.response = self.session.post(
            self.url,
            json=payload,
            stream=True
        )
        
        # Check for errors
        if self.response.status_code != 200:
            error_message = f"Streaming request failed with status {self.response.status_code}: {self.response.text}"
            logger.error(error_message)
            raise Exception(error_message)
        
        # Initialize the iterator
        self._iterator = self.response.iter_lines()
        
        return self
    
    def __next__(self) -> Dict[str, Any]:
        """
        Get the next chunk from the stream.
        
        Returns:
            Parsed JSON chunk
            
        Raises:
            StopIteration: When the stream is complete
        """
        if self._iterator is None:
            self.__iter__()
        
        # Get the next line
        line = next(self._iterator)
        
        # Skip empty lines
        while not line:
            line = next(self._iterator)
        
        # Parse the JSON
        try:
            chunk = json.loads(line.decode('utf-8'))
            return chunk
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON from stream: {line}")
            return {"error": "Invalid JSON", "raw": line.decode('utf-8')}
    
    def close(self):
        """Close the stream."""
        if self.response:
            self.response.close()
    
    def __enter__(self):
        """Support for context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support for context manager."""
        self.close()

def stream_generator(client, prompt: str, **kwargs) -> Iterator[str]:
    """
    Generator function for streaming text completions.
    
    This is a convenience function that yields only the text chunks
    from a streaming response.
    
    Args:
        client: SecureModelClient instance
        prompt: Text prompt
        **kwargs: Additional parameters for generate()
        
    Yields:
        Text chunks
    """
    # Ensure streaming is enabled
    kwargs["streaming"] = True
    
    # Get the stream
    stream = client.generate(prompt=prompt, **kwargs)
    
    # Yield text chunks
    for chunk in stream:
        if "text" in chunk:
            yield chunk["text"]
