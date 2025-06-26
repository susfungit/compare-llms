import os
import streamlit as st
import anthropic
from openai import OpenAI
from google import genai
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

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
    return completion.choices[0].message.content

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
    return completion.content[0].text

def generate_gemini_text(prompt, model):
    GEMINI_KEY = os.getenv("GEMINI_KEY")
    client = genai.Client(api_key=GEMINI_KEY)
    response = client.models.generate_content(model=model, contents=prompt)
    return response.text

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
    return completion.choices[0].message.content

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
    try:
        response = model_func(prompt, model_name)
        return model_name, response, None
    except Exception as e:
        return model_name, None, str(e)

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
                    model_name, response, error = future.result()
                    idx = name_to_index[model_name]
                    results[idx] = (model_name, response, error)

            # Display results in the same order as selected_models
            for i, (model_name, response, error) in enumerate(results):
                with cols[i]:
                    st.markdown(f"#### {model_name}")
                    if error:
                        st.error(f"Error for {model_name}: {error}")
                    else:
                        st.markdown(
                            f"""
                            <div class="boxed">
                                <div style='white-space: pre-wrap; font-family: inherit; font-size: 1rem;'>
                                    {response}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
        else:
            st.warning("Please enter a prompt before generating responses.")

if __name__ == "__main__":
    main()

