import os
from openai import OpenAI
from typing import Tuple
from .base import BaseModel, TokenInfo

class GrokModel(BaseModel):
    """xAI Grok model implementation."""
    
    def _create_client(self):
        """Create xAI client (OpenAI-compatible)."""
        xai_api_key = os.getenv("XAI_API_KEY")
        if not xai_api_key:
            raise ValueError("XAI_API_KEY environment variable not set")
        
        return OpenAI(
            api_key=xai_api_key,
            base_url="https://api.x.ai/v1"
        )
    
    def _generate_response(self, prompt: str) -> Tuple[str, TokenInfo]:
        """Generate response using Grok API."""
        completion = self.client.chat.completions.create(
            model=self.model_name,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        
        usage = completion.usage
        token_info = TokenInfo(
            input_tokens=usage.prompt_tokens,
            output_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens
        )
        
        return completion.choices[0].message.content, token_info 