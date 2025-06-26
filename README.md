# ChatGPT Model Comparison

This is a Streamlit web application that allows you to compare responses from multiple large language models (LLMs) side by side. Enter a prompt, select which models to compare, and view their responses in a visually organized way.

## Features
- Compare responses from OpenAI GPT, Anthropic Claude, Google Gemini, and xAI Grok models.
- Select which models to include in the comparison.
- View all responses in a clean, boxed, side-by-side layout.

## Supported Models
- OpenAI: `gpt-4o`, `chatgpt-4o-latest`, `o1`, `o3-mini`
- Google: `gemini-2.0-flash`
- xAI: `grok-2-latest`
- Anthropic: `claude-3-7-sonnet-20250219`

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
- **Google Gemini**: `GEMINI_KEY`
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

## License
MIT 