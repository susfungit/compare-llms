import os
import streamlit as st
import anthropic
from openai import OpenAI
from google import genai

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

def main():
    st.title("ChatGPT Model Comparison")
    
    # Prompt area
    prompt = st.text_area("Enter your prompt:", height=150)

    # List of models to choose from
    MODELS = [
        ("gpt-4o", generate_gpt_text),
        ("chatgpt-4o-latest", generate_gpt_text),
        ("o1", generate_gpt_text),
	("o3-mini",generate_gpt_text),
        ("gemini-2.0-flash", generate_gemini_text),
	("grok-2-latest",generate_grok_text),
	("claude-3-7-sonnet-20250219",generate_claude_text),
    ]

    st.subheader("Select the models you want to compare:")

    # Create columns for each model’s checkbox so they appear horizontally
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

            # Some custom CSS for a "boxed" look
            st.markdown(
                """
                <style>
                .boxed {
                    border: 1px solid rgba(49,51,63,0.2);
                    border-radius: 6px;
                    padding: 10px;
                    margin: 10px 0;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            # Generate and display each response
            for i, (model_name, model_func) in enumerate(selected_models):
                with cols[i]:
                    st.markdown(f"#### {model_name}")
                    try:
                        response = model_func(prompt, model_name)
                        st.markdown(
                            f"""
                            <div class="boxed">
                                {response}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    except Exception as e:
                        st.error(f"Error for {model_name}: {str(e)}")
        else:
            st.warning("Please enter a prompt before generating responses.")

if __name__ == "__main__":
    main()

