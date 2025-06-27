import streamlit as st
import warnings
import logging
import os
from typing import List

# Suppress warnings and logging
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)
logging.getLogger('absl').setLevel(logging.ERROR)
logging.getLogger('google').setLevel(logging.ERROR)
logging.getLogger('grpc').setLevel(logging.ERROR)
os.environ['GRPC_PYTHON_LOG_LEVEL'] = 'error'

# Import modular components
from config.settings import ConfigManager
from models.model_factory import ModelFactory
from utils.parallel_executor import ParallelExecutor
from ui.components import ModelSelector, ResponseDisplay, PromptInput, CustomCSS

class LLMComparisonApp:
    """Main application class for LLM comparison tool."""
    
    def __init__(self):
        """Initialize the application with required components."""
        self.config_manager = ConfigManager()
        self.model_factory = ModelFactory()
        self.executor = ParallelExecutor()
        
        # Configure Streamlit
        st.set_page_config(
            layout="wide", 
            page_title="LLM Model Comparison",
            page_icon="🤖"
        )
    
    def run(self):
        """Run the main application."""
        # Render custom CSS
        CustomCSS.render()
        
        # App header
        st.title("🤖 LLM Model Comparison")
        st.markdown("Compare responses from multiple Large Language Models side by side.")
        
        # Load and validate configuration
        try:
            models = self.config_manager.get_enabled_models()
            if not models:
                st.error("No enabled models found in configuration.")
                return
                
            # Validate configuration
            issues = self.config_manager.validate_config()
            if issues:
                with st.expander("⚠️ Configuration Issues", expanded=False):
                    for issue in issues:
                        st.warning(issue)
                        
        except Exception as e:
            st.error(f"Configuration error: {e}")
            st.info("Please check your models_config.json file.")
            return
        
        # Prompt input
        prompt = PromptInput.render()
        
        # Model selection
        st.subheader("📋 Select models to compare:")
        model_selections = ModelSelector.render(models)
        selected_models = ModelSelector.get_selected_models(models, model_selections)
        
        # Validation
        if not selected_models:
            st.warning("⚠️ Please select at least one model.")
            return
        
        # Generate responses button
        if st.button("🚀 Generate Responses", type="primary"):
            self._handle_generation(prompt, selected_models)
    
    def _handle_generation(self, prompt: str, selected_models: List):
        """Handle the response generation process."""
        if not prompt.strip():
            st.warning("⚠️ Please enter a prompt before generating responses.")
            return
        
        st.subheader(f"📊 Comparing responses from {len(selected_models)} models:")
        
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Update status
            status_text.text("🔄 Initializing models...")
            progress_bar.progress(0.2)
            
            # Create model instances
            model_instances = []
            for model_config in selected_models:
                try:
                    model = self.model_factory.create_model(
                        model_config.name, 
                        model_config.provider
                    )
                    model_instances.append(model)
                except Exception as e:
                    st.error(f"Failed to initialize {model_config.name}: {e}")
                    return
            
            # Update status
            status_text.text("⚡ Generating responses in parallel...")
            progress_bar.progress(0.4)
            
            # Generate responses in parallel
            responses = self.executor.execute_parallel(model_instances, prompt)
            
            # Update status
            progress_bar.progress(1.0)
            status_text.text("✅ Generation complete!")
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Display results
            ResponseDisplay.render(responses)
            
            # Show summary statistics
            self._show_summary(responses)
            
        except Exception as e:
            st.error(f"Error during generation: {e}")
            progress_bar.empty()
            status_text.empty()
    
    def _show_summary(self, responses: List):
        """Show summary statistics of the responses."""
        if not responses:
            return
        
        with st.expander("📈 Summary Statistics", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            
            # Calculate statistics
            successful_responses = [r for r in responses if not r.error]
            failed_responses = [r for r in responses if r.error]
            
            if successful_responses:
                avg_time = sum(r.elapsed_time for r in successful_responses) / len(successful_responses)
                fastest = min(successful_responses, key=lambda r: r.elapsed_time)
                slowest = max(successful_responses, key=lambda r: r.elapsed_time)
                
                with col1:
                    st.metric("✅ Successful", len(successful_responses))
                
                with col2:
                    st.metric("⚡ Average Time", f"{avg_time:.2f}s")
                
                with col3:
                    st.metric("🏃 Fastest", f"{fastest.model_name} ({fastest.elapsed_time:.2f}s)")
                
                with col4:
                    st.metric("🐌 Slowest", f"{slowest.model_name} ({slowest.elapsed_time:.2f}s)")
            
            if failed_responses:
                st.error(f"❌ {len(failed_responses)} model(s) failed to generate responses")

def main():
    """Main entry point."""
    try:
        app = LLMComparisonApp()
        app.run()
    except Exception as e:
        st.error(f"Application error: {e}")
        st.info("Please check your configuration and try again.")

if __name__ == "__main__":
    main() 