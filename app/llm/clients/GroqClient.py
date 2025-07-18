import os
from typing import Optional, Dict, Any
from langchain_groq import ChatGroq
from langchain_core.language_models.llms import LLM
from ..LLMProvider import LLMProvider


class GroqClient(LLMProvider):
    
    _instance: Optional['GroqClient'] = None # Cached Provider instances
    _llm_instance: Optional[LLM] = None # Cached LLM instance
    
    def __new__(cls) -> 'GroqClient':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._api_key = os.getenv('GROQ_API_KEY')
            self._default_model = os.getenv('GROQ_MODEL', 'llama3-8b-8192')
            self._default_temperature = float(os.getenv('GROQ_TEMPERATURE', '0.7'))
            self._default_max_tokens = int(os.getenv('GROQ_MAX_TOKENS', '1024'))
            
            if not self._api_key:
                raise ValueError("GROQ_API_KEY environment variable is required")
    
    def create_llm(self, **kwargs) -> LLM:
        """
        Configuration parameters for the LLM
            - model: Model name (default: llama3-8b-8192)
            - temperature: Temperature for generation (default: 0.7)
            - max_tokens: Maximum tokens to generate (default: 1024)
            - top_p: Top-p sampling parameter
            - frequency_penalty: Frequency penalty
            - presence_penalty: Presence penalty
            - stop: Stop sequences
        """
        config = {
            'groq_api_key': self._api_key,
            'model_name': kwargs.get('model', self._default_model),
            'temperature': kwargs.get('temperature', self._default_temperature),
            'max_tokens': kwargs.get('max_tokens', self._default_max_tokens),
        }
        
        optional_params = ['top_p', 'frequency_penalty', 'presence_penalty', 'stop']
        for param in optional_params:
            if param in kwargs:
                config[param] = kwargs[param]
        
        return ChatGroq(**config)
    
    def get_llm(self) -> LLM:
        if self._llm_instance is None:
            self._llm_instance = self.create_llm()
        return self._llm_instance
    
    @property
    def current_config(self) -> Dict[str, Any]:
        return {
            'model': self._default_model,
            'temperature': self._default_temperature,
            'max_tokens': self._default_max_tokens,
            'api_key_set': bool(self._api_key),
        }
        
        
"""
available models:
'llama3-8b-8192',
'llama3-70b-8192',
'mixtral-8x7b-32768',
'gemma-7b-it',
'gemma2-9b-it',
"""