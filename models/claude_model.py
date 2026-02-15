import anthropic
from typing import Tuple
from .base import BaseModel, TokenInfo

class ClaudeModel(BaseModel):
    """Anthropic Claude model implementation."""
    
    def _create_client(self):
        """Create Anthropic client."""
        return anthropic.Anthropic()
    
    def _generate_response(self, prompt: str) -> Tuple[str, TokenInfo]:
        """Generate response using Claude API."""
        completion = self.client.messages.create(
            model=self.model_name,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        
        usage = completion.usage
        token_info = TokenInfo(
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            total_tokens=usage.input_tokens + usage.output_tokens
        )
        
        return completion.content[0].text, token_info 
