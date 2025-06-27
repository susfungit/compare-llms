# ChatGPT Model Comparison

This is a Streamlit web application that allows you to compare responses from multiple large language models (LLMs) side by side. Enter a prompt, select which models to compare, and view their responses in a visually organized way.

## Features
- Compare responses from OpenAI GPT, Anthropic Claude, Google Gemini (via the latest google-genai SDK), and xAI Grok models.
- Select which models to include in the comparison.
- View all responses in a clean, boxed, side-by-side layout.
- **Easily add or remove models by editing `models_config.json`.**
- **Faster results: LLM requests are now executed in parallel for improved efficiency.**
- **Each model's response is shown in a clearly visible, scrollable, bordered rectangle with a white background and dark text for readability.**
- **Response timing and token usage statistics for each model (input tokens, output tokens, and total tokens).**

## Supported Models
The list of supported models is maintained in the `models_config.json` file. Each entry specifies the model name and its provider. Example:

```json
[
  {"name": "gpt-4o", "provider": "openai"},
  {"name": "gemini-2.0-flash", "provider": "gemini"}
]
```

To add a new model, simply add a new object to this list with the appropriate `name` and `provider`.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo-url>
cd compare-llms
```

### 2. Install Dependencies
It is recommended to use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set API Keys
You need API keys for each provider you want to use. Set the following environment variables:

- **OpenAI**: `OPENAI_API_KEY`
- **Anthropic**: `ANTHROPIC_API_KEY`
- **Google Gemini**: `GEMINI_KEY` (set in your environment; the google-genai client will use it automatically if present)
- **xAI Grok**: `XAI_API_KEY`

You can set them in your shell or in a `.env` file (if using a tool like `python-dotenv`). Example:
```bash
export OPENAI_API_KEY=your-openai-key
export ANTHROPIC_API_KEY=your-anthropic-key
export GEMINI_KEY=your-gemini-key
export XAI_API_KEY=your-xai-key
```

### 4. Run the App
```bash
streamlit run main.py
```

The app will open in your browser. Enter a prompt, select models, and click "Generate Responses" to compare outputs.

## Notes
- Make sure you have valid API keys for the models you want to use.
- Some models may require access approval or billing setup with the provider.
- If you encounter errors, check your API keys and provider access.
- To add or remove models, simply edit the `models_config.json` file and restart the app.
- LLM requests are executed in parallel using Python's `concurrent.futures` (part of the standard library, no extra install needed).
- Each model's response is displayed in a scrollable, bordered window for easy reading and comparison.
- Token usage statistics show input tokens, output tokens, and total tokens for each response. Models that don't provide this information will display "Not available".
- **Gemini integration now uses the latest [google-genai](https://pypi.org/project/google-genai/) SDK with `genai.Client` and `genai.types`.**

## License
MIT 