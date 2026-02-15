from openai import OpenAI
from typing import Tuple
from .base import BaseModel, TokenInfo

class OpenAIModel(BaseModel):
    """OpenAI GPT model implementation."""
    
    def _create_client(self):
        """Create OpenAI client."""
        return OpenAI()
    
    def _generate_response(self, prompt: str) -> Tuple[str, TokenInfo]:
        """Generate response using OpenAI API."""
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