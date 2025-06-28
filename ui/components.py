import streamlit as st
from typing import List, Dict, Any
from config.settings import ModelConfig
from models.base import ModelResponse

class ModelSelector:
    """Component for selecting models to compare."""
    
    @staticmethod
    def render(models: List[ModelConfig]) -> Dict[str, bool]:
        """
        Render model selection checkboxes.
        
        Args:
            models: List of model configurations
            
        Returns:
            Dictionary mapping model IDs to selection status
        """
        if not models:
            st.warning("No models available in configuration.")
            return {}
        
        # Create columns for checkboxes
        cols = st.columns(len(models))
        selections = {}
        
        for i, model in enumerate(models):
            with cols[i]:
                # Use display_name for UI, model_id for internal logic
                selections[model.model_id] = st.checkbox(
                    model.display_name, 
                    value=True,
                    key=f"model_select_{model.model_id}"
                )
        
        return selections
    
    @staticmethod
    def get_selected_models(models: List[ModelConfig], selections: Dict[str, bool]) -> List[ModelConfig]:
        """Get list of selected models."""
        return [model for model in models if selections.get(model.model_id, False)]

class ResponseDisplay:
    """Component for displaying model responses."""
    
    @staticmethod
    def render(responses: List[ModelResponse]):
        """
        Render all model responses in columns.
        
        Args:
            responses: List of model responses to display
        """
        if not responses:
            st.info("No responses to display.")
            return
        
        # Create columns for responses
        cols = st.columns(len(responses))
        
        for i, response in enumerate(responses):
            ResponseDisplay._render_single_response(response, cols[i], i)
    
    @staticmethod
    def _render_single_response(response: ModelResponse, col, index: int):
        """Render a single model response."""
        with col:
            st.markdown(f"#### {response.model_name}")
            
            if response.error:
                st.error(f"Error: {response.error}")
                ResponseDisplay._render_error_stats(response)
            else:
                # Display response text
                st.text_area(
                    "Response:",
                    value=response.text,
                    height=200,
                    disabled=True,
                    key=f"response_{index}"
                )
                
                # Display statistics
                ResponseDisplay._render_stats(response)
    
    @staticmethod
    def _render_stats(response: ModelResponse):
        """Render response statistics."""
        token_display = ResponseDisplay._format_token_info(response.token_info)
        
        st.markdown(
            f"""
            <div style='font-size: 0.8em; color: #666; margin-top: 5px; 
                       padding: 5px; background: #f8f9fa; border-radius: 4px;'>
                ⏱️ {response.elapsed_time:.2f}s | {token_display}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def _render_error_stats(response: ModelResponse):
        """Render statistics for error responses."""
        st.markdown(
            f"""
            <div style='font-size: 0.8em; color: #888; margin-top: 5px;'>
                ⏱️ Time: {response.elapsed_time:.2f} seconds
            </div>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def _format_token_info(token_info) -> str:
        """Format token information for display."""
        if not token_info:
            return "📊 Tokens: Not available"
        
        if (token_info.total_tokens not in ['Not available', 'Error'] and 
            isinstance(token_info.total_tokens, int)):
            return (f"📊 Tokens: {token_info.input_tokens} in, "
                   f"{token_info.output_tokens} out ({token_info.total_tokens} total)")
        else:
            return f"📊 Tokens: {token_info.total_tokens}"

class PromptInput:
    """Component for prompt input."""
    
    @staticmethod
    def render(height: int = 150, placeholder: str = "Enter your prompt here...") -> str:
        """
        Render prompt input text area.
        
        Args:
            height: Height of the text area
            placeholder: Placeholder text
            
        Returns:
            The entered prompt text
        """
        return st.text_area(
            "Enter your prompt:",
            height=height,
            placeholder=placeholder,
            key="prompt_input"
        )

class CustomCSS:
    """Component for rendering custom CSS styles."""
    
    @staticmethod
    def render():
        """Render custom CSS for the application."""
        st.markdown(
            """
            <style>
            .response-container {
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                padding: 12px;
                margin: 10px 0;
                background: #fff;
                color: #222;
                min-height: 180px;
                max-height: 400px;
                overflow-y: auto;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            }
            
            .model-header {
                color: #1f2937;
                font-weight: 600;
                margin-bottom: 10px;
            }
            
            .stats-container {
                font-size: 0.8em;
                color: #666;
                margin-top: 5px;
                padding: 5px;
                background: #f8f9fa;
                border-radius: 4px;
                border-left: 3px solid #007bff;
            }
            
            .error-container {
                background: #fff5f5;
                border-left: 3px solid #ef4444;
            }
            </style>
            """,
            unsafe_allow_html=True
        ) 