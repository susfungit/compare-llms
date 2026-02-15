# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
streamlit run main.py
```

Requires API keys as environment variables: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_KEY`, `XAI_API_KEY`.

## Dependencies

```bash
pip install -r requirements.txt
```

Key dependencies: streamlit, openai, anthropic, google-genai.

## Architecture

This is a Streamlit app that compares responses from multiple LLM providers side by side with parallel execution and token/timing metrics.

### Core Flow
`main.py` → `LLMComparisonApp` orchestrates everything: loads config, renders UI, creates model instances via factory, executes requests in parallel, displays results.

### Key Modules
- **`models/base.py`**: `BaseModel` ABC that all providers extend. Subclasses implement `_create_client()` and `_generate_response()`. The base `generate()` method handles timing and error wrapping into `ModelResponse`.
- **`models/model_factory.py`**: `ModelFactory` maps provider strings to model classes. To add a new provider: create a model class extending `BaseModel`, then register it in `ModelFactory._model_classes`.
- **`config/settings.py`**: `ConfigManager` loads `models_config.json`. `ModelConfig` dataclass holds `model_id`, `provider`, `display_name`, `enabled`, `max_tokens`, `temperature`.
- **`utils/parallel_executor.py`**: `ParallelExecutor` uses `ThreadPoolExecutor` to call `model.generate(prompt)` concurrently, preserving input order in results.
- **`ui/components.py`**: Streamlit UI components (`ModelSelector`, `ResponseDisplay`, `PromptInput`, `CustomCSS`).

### Model Configuration
Models are defined in `models_config.json` as a flat JSON array. Each entry has `model_id` (sent to the API), `provider` (maps to factory), and `display_name` (shown in UI). Add/remove models by editing this file — no code changes needed.

### Supported Providers
Four providers with matching env vars: `openai`, `claude` (Anthropic), `gemini` (Google), `grok` (xAI). Each has a model class in `models/` following the same pattern.

### Important Pattern
`display_name` is used for UI display; `model_id` is what gets sent to the LLM API. These are mapped in `main.py:_handle_generation` after parallel execution completes.
