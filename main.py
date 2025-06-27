import os
import streamlit as st
import anthropic
from openai import OpenAI
import google.generativeai as genai
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import html

# Switch to wide layout
st.set_page_config(layout="wide")

def generate_gpt_text(prompt, model):
    client = OpenAI()
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    # Extract token usage
    usage = completion.usage
    token_info = {
        'input_tokens': usage.prompt_tokens,
        'output_tokens': usage.completion_tokens,
        'total_tokens': usage.total_tokens
    }
    return completion.choices[0].message.content, token_info

def generate_claude_text(prompt, model):
    client = anthropic.Anthropic()
    completion = client.messages.create(
        model=model,
	max_tokens=1000,
	temperature=1,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    # Extract token usage
    usage = completion.usage
    token_info = {
        'input_tokens': usage.input_tokens,
        'output_tokens': usage.output_tokens,
        'total_tokens': usage.input_tokens + usage.output_tokens
    }
    return completion.content[0].text, token_info

def generate_gemini_text(prompt, model):
    try:
        GEMINI_KEY = os.getenv("GEMINI_KEY")
        if not GEMINI_KEY:
            raise ValueError("GEMINI_KEY environment variable not set")
        
        genai.configure(api_key=GEMINI_KEY)
        model_instance = genai.GenerativeModel(model)
        response = model_instance.generate_content(prompt)
        
        # Check if response has text
        if hasattr(response, 'text'):
            response_text = response.text
        else:
            response_text = str(response)
            
        # Debug: print the response to see what we're getting
        print(f"Gemini response type: {type(response_text)}")
        print(f"Gemini response content: {response_text[:200]}...")
            
        # Gemini doesn't provide token usage in the same way
        token_info = {
            'input_tokens': 'Not available',
            'output_tokens': 'Not available',
            'total_tokens': 'Not available'
        }
        return response_text, token_info
    except Exception as e:
        raise Exception(f"Gemini API error: {str(e)}")

def generate_grok_text(prompt,model):
    XAI_API_KEY=os.getenv("XAI_API_KEY")
    client = OpenAI(
	api_key=XAI_API_KEY,
	base_url="https://api.x.ai/v1",
	)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    # Extract token usage (xAI uses OpenAI-compatible API)
    usage = completion.usage
    token_info = {
        'input_tokens': usage.prompt_tokens,
        'output_tokens': usage.completion_tokens,
        'total_tokens': usage.total_tokens
    }
    return completion.choices[0].message.content, token_info

def get_model_function(provider):
    if provider == "openai":
        return generate_gpt_text
    elif provider == "claude":
        return generate_claude_text
    elif provider == "gemini":
        return generate_gemini_text
    elif provider == "grok":
        return generate_grok_text
    else:
        raise ValueError(f"Unknown provider: {provider}")

def get_response(model_func, prompt, model_name):
    start_time = time.time()
    try:
        response, token_info = model_func(prompt, model_name)
        elapsed = time.time() - start_time
        return model_name, response, None, elapsed, token_info
    except Exception as e:
        elapsed = time.time() - start_time
        token_info = {
            'input_tokens': 'Error',
            'output_tokens': 'Error',
            'total_tokens': 'Error'
        }
        return model_name, None, str(e), elapsed, token_info

def main():
    st.title("ChatGPT Model Comparison")
    
    # Prompt area
    prompt = st.text_area("Enter your prompt:", height=150)

    # Load models from config file
    with open("models_config.json", "r") as f:
        models_config = json.load(f)
    MODELS = [(m["name"], get_model_function(m["provider"])) for m in models_config]

    st.subheader("Select the models you want to compare:")

    # Create columns for each model's checkbox so they appear horizontally
    checkbox_cols = st.columns(len(MODELS))
    model_selections = {}
    for i, (model_name, _) in enumerate(MODELS):
        with checkbox_cols[i]:
            model_selections[model_name] = st.checkbox(model_name, value=True)

    # Button to generate responses
    if st.button("Generate Responses"):
        # Filter selected models
        selected_models = [m for m in MODELS if model_selections[m[0]]]

        # Make sure user selected at least one model
        if not selected_models:
            st.warning("Please select at least one model.")
            return

        # Ensure user has actually entered a prompt
        if prompt:
            st.subheader("Comparing responses from selected models:")

            # Create columns for each selected model
            cols = st.columns(len(selected_models))

            # Some custom CSS for a "boxed" look with scrollbars and fixed height
            st.markdown(
                """
                <style>
                .boxed {
                    border: 2px solid #888;
                    border-radius: 8px;
                    padding: 12px;
                    margin: 10px 0;
                    background: #fff;
                    color: #222;
                    min-height: 180px;
                    max-height: 350px;
                    overflow-y: auto;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            # Parallel execution for model responses
            futures = []
            with ThreadPoolExecutor() as executor:
                for model_name, model_func in selected_models:
                    futures.append(executor.submit(get_response, model_func, prompt, model_name))
                results = [None] * len(selected_models)
                name_to_index = {model_name: i for i, (model_name, _) in enumerate(selected_models)}
                for future in as_completed(futures):
                    model_name, response, error, elapsed, token_info = future.result()
                    idx = name_to_index[model_name]
                    results[idx] = (model_name, response, error, elapsed, token_info)

            # Display results in the same order as selected_models
            for i, (model_name, response, error, elapsed, token_info) in enumerate(results):
                with cols[i]:
                    st.markdown(f"#### {model_name}")
                    if error:
                        st.error(f"Error for {model_name}: {error}")
                        st.markdown(f"<span style='color: #888;'>⏱️ Time: {elapsed:.2f} seconds</span>", unsafe_allow_html=True)
                    else:
                        # Format token info for display
                        if token_info['total_tokens'] != 'Not available' and token_info['total_tokens'] != 'Error':
                            token_display = f"📊 Tokens: {token_info['input_tokens']} in, {token_info['output_tokens']} out ({token_info['total_tokens']} total)"
                        else:
                            token_display = f"📊 Tokens: {token_info['total_tokens']}"
                        
                        # Display response and stats
                        # Display response as plain text
                        st.text_area("Response:", value=response, height=200, disabled=True, key=f"response_{i}")
                        # Display stats below response in a smaller format
                        st.markdown(
                            f"""
                            <div style='font-size: 0.8em; color: #666; margin-top: 5px; padding: 5px; background: #f8f9fa; border-radius: 4px;'>
                                ⏱️ {elapsed:.2f}s | {token_display}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
        else:
            st.warning("Please enter a prompt before generating responses.")

if __name__ == "__main__":
    main()

