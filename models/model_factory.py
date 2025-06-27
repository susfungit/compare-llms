from typing import Dict, Type
from .base import BaseModel
from .openai_model import OpenAIModel
from .claude_model import ClaudeModel
from .gemini_model import GeminiModel
from .grok_model import GrokModel

class ModelFactory:
    """Factory class to create model instances based on provider."""
    
    _model_classes: Dict[str, Type[BaseModel]] = {
        "openai": OpenAIModel,
        "claude": ClaudeModel,
        "gemini": GeminiModel,
        "grok": GrokModel
    }
    
    @classmethod
    def create_model(cls, model_name: str, provider: str) -> BaseModel:
        """Create a model instance based on provider."""
        if provider not in cls._model_classes:
            raise ValueError(f"Unknown provider: {provider}")
        
        model_class = cls._model_classes[provider]
        return model_class(model_name)
    
    @classmethod
    def get_supported_providers(cls) -> list:
        """Get list of supported providers."""
        return list(cls._model_classes.keys())
    
    @classmethod
    def register_model(cls, provider: str, model_class: Type[BaseModel]):
        """Register a new model provider (for extensibility)."""
        cls._model_classes[provider] = model_class 