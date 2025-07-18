import requests
import json
import numpy as np
from typing import List, Union, Optional
import time
import logging
import os

class EmbeddingHandler:
    
    def __init__(self, 
                 model_name: Optional[str] = None,
                 api_token: Optional[str] = None,
                 max_retries: int = 3,
                 retry_delay: float = 1.0):

        # Get environment variables or use defaults
        hf_url = os.getenv("HF_URL")
        model_name = model_name or os.getenv("HF_MODEL")
        api_token = api_token or os.getenv("HF_API_KEY")

        self.model_name = model_name
        self.api_token = api_token
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Hugging Face Inference API endpoint
        self.api_url = f"{hf_url}/{model_name}"
        # Set up headers
        self.headers = {
            "Content-Type": "application/json"
        }
        
        if self.api_token:
            self.headers["Authorization"] = f"Bearer {self.api_token}"
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _make_request(self, texts: List[str]) -> List[List[float]]:
        payload = {
            "inputs": texts,
            "options": {
                "wait_for_model": True,
                "use_cache": True
            }
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    embeddings = response.json()
                    return embeddings
                elif response.status_code == 503:
                    # Model is loading, wait and retry
                    self.logger.warning(f"Model is loading, waiting {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    self.logger.error(f"API request failed with status {response.status_code}: {response.text}")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                        continue
                    else:
                        raise Exception(f"API request failed: {response.status_code} - {response.text}")
                        
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request exception: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise
        
        raise Exception(f"Failed to get embeddings after {self.max_retries} attempts")
    
    def get_embeddings(self, texts: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
       try:
            # Handle single string input
            if isinstance(texts, str):
                texts = [texts]
                return_single = True
            else:
                return_single = False
            
            # Validate input
            if not texts or len(texts) == 0:
                raise ValueError("Input texts cannot be empty")
            
            # Make API request
            embeddings = self._make_request(texts)
            
            # Return single embedding if single input was provided
            if return_single:
                return embeddings[0]
            
            return embeddings
       except Exception as e:
            self.logger.error(f"Error getting embeddings: {e}")
            raise e
   