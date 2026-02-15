# LLM Model Comparison Tool

A Streamlit web application for comparing responses from multiple LLM providers side by side with parallel execution and token/timing metrics.

## Features

- **Multi-Model Comparison**: Compare responses from OpenAI, Anthropic Claude, Google Gemini, and xAI Grok models
- **Parallel Processing**: All LLM requests execute simultaneously
- **Performance Metrics**: Response timing and token usage statistics for each model
- **Configuration-Driven**: Add/remove models by editing `models_config.json` — no code changes needed
- **Model Availability Checker**: Verify configured models and discover new ones via `check_models.py`

## Project Structure

```
compare-llms/
├── main.py                    # App entry point (LLMComparisonApp)
├── check_models.py            # Model availability checker
├── models/                    # Model implementations
│   ├── base.py               # BaseModel ABC
│   ├── openai_model.py       # OpenAI GPT models
│   ├── claude_model.py       # Anthropic Claude models
│   ├── gemini_model.py       # Google Gemini models
│   ├── grok_model.py         # xAI Grok models
│   └── model_factory.py      # Factory mapping providers to classes
├── config/
│   └── settings.py           # ConfigManager, ModelConfig dataclass
├── ui/
│   └── components.py         # Streamlit UI components
├── utils/
│   └── parallel_executor.py  # ThreadPoolExecutor wrapper
├── models_config.json        # Model configuration
└── requirements.txt
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
```bash
export OPENAI_API_KEY=your-openai-key
export ANTHROPIC_API_KEY=your-anthropic-key
export GOOGLE_API_KEY=your-gemini-key
export XAI_API_KEY=your-xai-key
```

You only need keys for the providers you want to use. Models from providers without keys will be skipped.

### 3. Run the Application
```bash
streamlit run main.py
```

## Model Configuration

Models are defined in `models_config.json` as a flat array:

```json
[
  {"model_id": "gpt-4o", "provider": "openai", "display_name": "gpt-4o"},
  {"model_id": "claude-sonnet-4-20250514", "provider": "claude", "display_name": "claude sonnet 4"},
  {"model_id": "gemini-2.5-flash", "provider": "gemini", "display_name": "gemini-2.5-flash"},
  {"model_id": "grok-3", "provider": "grok", "display_name": "grok-3"}
]
```

Each entry has:
- `model_id` — the ID sent to the provider's API
- `provider` — one of `openai`, `claude`, `gemini`, `grok`
- `display_name` — label shown in the UI

Optional fields: `enabled` (default `true`), `max_tokens` (default `1000`), `temperature` (default `1.0`).

### Check Model Availability

Run the checker to verify configured models still exist and discover new ones:

```bash
python check_models.py
```

Output shows valid models, deprecated/missing models, and new models available from each provider.

## Adding a New Provider

1. Create a model class in `models/` extending `BaseModel`
2. Implement `_create_client()` and `_generate_response()`
3. Register it in `ModelFactory._model_classes`
4. Add models to `models_config.json`

## Troubleshooting

- **API key issues**: Verify environment variables are set correctly
- **Model failures**: Check API key permissions and quotas
- **Configuration errors**: Validate `models_config.json` syntax; run `python check_models.py` to verify model IDs

## Links
- [OpenAI API](https://platform.openai.com/docs)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [Google Gemini API](https://ai.google.dev/)
- [xAI Grok API](https://docs.x.ai/)
- [Streamlit](https://docs.streamlit.io/)
