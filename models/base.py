from abc import ABC, abstractmethod
from typing import Dict, Tuple, Any, Union
from dataclasses import dataclass
import time

@dataclass
class TokenInfo:
    input_tokens: Union[int, str]
    output_tokens: Union[int, str]
    total_tokens: Union[int, str]

@dataclass
class ModelResponse:
    model_name: str
    text: str = None
    token_info: TokenInfo = None
    elapsed_time: float = 0.0
    error: str = None

class BaseModel(ABC):
    """Base class for all LLM models."""
    
    def __init__(self, model_name: str, max_tokens: int = 1000, temperature: float = 1.0):
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self._client = None
    
    @property
    def client(self):
        """Lazy loading of client to avoid unnecessary connections."""
        if self._client is None:
            self._client = self._create_client()
        return self._client
    
    @abstractmethod
    def _create_client(self):
        """Create and return the API client for this model."""
        pass
    
    @abstractmethod
    def _generate_response(self, prompt: str) -> Tuple[str, TokenInfo]:
        """Generate response from the model. Must be implemented by subclasses."""
        pass
    
    def generate(self, prompt: str) -> ModelResponse:
        """Generate response with timing and error handling."""
        start_time = time.time()
        
        try:
            text, token_info = self._generate_response(prompt)
            elapsed = time.time() - start_time
            return ModelResponse(
                model_name=self.model_name,
                text=text,
                token_info=token_info,
                elapsed_time=elapsed
            )
        except Exception as e:
            elapsed = time.time() - start_time
            error_token_info = TokenInfo(
                input_tokens='Error',
                output_tokens='Error',
                total_tokens='Error'
            )
            return ModelResponse(
                model_name=self.model_name,
                token_info=error_token_info,
                elapsed_time=elapsed,
                error=str(e)
            ) 