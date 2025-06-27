import json
import os
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class ModelConfig:
    """Configuration for a single model."""
    name: str
    provider: str
    enabled: bool = True
    max_tokens: int = 1000
    temperature: float = 1.0
    display_name: Optional[str] = None
    
    def __post_init__(self):
        if self.display_name is None:
            self.display_name = self.name

class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_file: str = "models_config.json"):
        self.config_file = config_file
        self._models = None
    
    @property
    def models(self) -> List[ModelConfig]:
        """Get all models from configuration."""
        if self._models is None:
            self._models = self._load_models()
        return self._models
    
    def _load_models(self) -> List[ModelConfig]:
        """Load models from configuration file."""
        try:
            if not os.path.exists(self.config_file):
                raise FileNotFoundError(f"Configuration file '{self.config_file}' not found")
            
            with open(self.config_file, 'r') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                raise ValueError("Configuration must be a list of model objects")
            
            models = []
            for model_data in data:
                if not isinstance(model_data, dict):
                    raise ValueError("Each model configuration must be an object")
                
                # Validate required fields
                required_fields = ['name', 'provider']
                for field in required_fields:
                    if field not in model_data:
                        raise ValueError(f"Model configuration missing required field: {field}")
                
                models.append(ModelConfig(**model_data))
            
            return models
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
        except Exception as e:
            raise ValueError(f"Error loading configuration: {e}")
    
    def get_enabled_models(self) -> List[ModelConfig]:
        """Get only enabled models."""
        return [m for m in self.models if m.enabled]
    
    def get_models_by_provider(self, provider: str) -> List[ModelConfig]:
        """Get models for a specific provider."""
        return [m for m in self.models if m.provider == provider]
    
    def get_model_by_name(self, name: str) -> Optional[ModelConfig]:
        """Get a specific model by name."""
        for model in self.models:
            if model.name == name:
                return model
        return None
    
    def reload_config(self):
        """Reload configuration from file."""
        self._models = None
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return list of issues."""
        issues = []
        
        try:
            models = self.models
            
            # Check for duplicate model names
            names = [m.name for m in models]
            duplicates = set([name for name in names if names.count(name) > 1])
            if duplicates:
                issues.append(f"Duplicate model names found: {duplicates}")
            
            # Check for supported providers
            from models.model_factory import ModelFactory
            supported_providers = ModelFactory.get_supported_providers()
            
            for model in models:
                if model.provider not in supported_providers:
                    issues.append(f"Unsupported provider '{model.provider}' for model '{model.name}'")
            
        except Exception as e:
            issues.append(f"Configuration validation error: {e}")
        
        return issues 