from google import genai
from google.genai import types
from typing import Tuple
from .base import BaseModel, TokenInfo

class GeminiModel(BaseModel):
    """Google Gemini model implementation."""
    
    def _create_client(self):
        """Create Gemini client."""
        return genai.Client()
    
    def _generate_response(self, prompt: str) -> Tuple[str, TokenInfo]:
        """Generate response using Gemini API."""
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=self.max_tokens,
                temperature=self.temperature,
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            )
        )
        
        token_info = TokenInfo(
            input_tokens='Not available',
            output_tokens='Not available',
            total_tokens='Not available'
        )
        
        return response.text, token_info 