from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Callable, Any
import logging

logger = logging.getLogger(__name__)

class ParallelExecutor:
    """Executes multiple tasks in parallel using ThreadPoolExecutor."""
    
    def __init__(self, max_workers: int = None):
        """
        Initialize the parallel executor.
        
        Args:
            max_workers: Maximum number of worker threads. If None, uses default.
        """
        self.max_workers = max_workers
    
    def execute_parallel(self, models: List[Any], prompt: str) -> List[Any]:
        """
        Execute model generation requests in parallel.
        
        Args:
            models: List of model instances with generate() method
            prompt: The prompt to send to all models
            
        Returns:
            List of ModelResponse objects in the same order as input models
        """
        if not models:
            return []
        
        results = [None] * len(models)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_index = {
                executor.submit(model.generate, prompt): i
                for i, model in enumerate(models)
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    result = future.result()
                    results[index] = result
                    logger.debug(f"Completed request for model at index {index}")
                except Exception as e:
                    logger.error(f"Error in model at index {index}: {e}")
                    # The model's generate method should already handle errors
                    # and return a ModelResponse with error information
                    results[index] = self._create_error_response(
                        models[index].model_name, str(e)
                    )
        
        return results
    
    def _create_error_response(self, model_name: str, error_msg: str):
        """Create a standardized error response."""
        from models.base import ModelResponse, TokenInfo
        
        error_token_info = TokenInfo(
            input_tokens='Error',
            output_tokens='Error',
            total_tokens='Error'
        )
        
        return ModelResponse(
            model_name=model_name,
            token_info=error_token_info,
            elapsed_time=0.0,
            error=error_msg
        ) 