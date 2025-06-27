# 🤖 LLM Model Comparison Tool

A powerful Streamlit web application that allows you to compare responses from multiple Large Language Models (LLMs) side by side. Enter a prompt, select which models to compare, and view their responses in a visually organized way with detailed performance metrics.

## ✨ Features

### Core Functionality
- **Multi-Model Comparison**: Compare responses from OpenAI GPT, Anthropic Claude, Google Gemini, and xAI Grok models
- **Parallel Processing**: All LLM requests execute simultaneously for faster results
- **Real-time Metrics**: Response timing and token usage statistics for each model
- **Clean UI**: Scrollable, bordered response windows with excellent readability

### Advanced Features
- **Modular Architecture**: Clean, maintainable code structure with separated concerns
- **Configuration-Driven**: Easily add/remove models via `models_config.json`
- **Error Handling**: Comprehensive error management with detailed feedback
- **Performance Analytics**: Summary statistics showing fastest/slowest models
- **Progress Tracking**: Real-time progress indicators during generation

## 🏗️ Project Structure

```
compare-llms/
├── main.py                    # Original monolithic version
├── main_modular.py           # New modular version (recommended)
├── models/                   # Model implementations
│   ├── base.py              # Abstract base class
│   ├── openai_model.py      # OpenAI GPT models
│   ├── claude_model.py      # Anthropic Claude models
│   ├── gemini_model.py      # Google Gemini models
│   ├── grok_model.py        # xAI Grok models
│   └── model_factory.py     # Model factory pattern
├── config/                  # Configuration management
│   └── settings.py          # Config loading and validation
├── ui/                      # UI components
│   └── components.py        # Reusable UI components
├── utils/                   # Utilities
│   └── parallel_executor.py # Parallel execution engine
├── models_config.json       # Model configuration
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repo-url>
cd compare-llms
```

### 2. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure API Keys
Set the following environment variables:

```bash
export OPENAI_API_KEY=your-openai-key
export ANTHROPIC_API_KEY=your-anthropic-key
export GEMINI_KEY=your-gemini-key
export XAI_API_KEY=your-xai-key
```

### 4. Run the Application

**Option A: Modular Version (Recommended)**
```bash
streamlit run main_modular.py
```

**Option B: Original Version**
```bash
streamlit run main.py
```

## ⚙️ Configuration

### Model Configuration
Models are configured in `models_config.json`:

```json
[
  {"name": "gpt-4o", "provider": "openai", "enabled": true},
  {"name": "claude-3-7-sonnet-20250219", "provider": "claude", "enabled": true},
  {"name": "gemini-2.0-flash", "provider": "gemini", "enabled": true},
  {"name": "grok-2-latest", "provider": "grok", "enabled": true}
]
```

### Adding New Models
1. Add entry to `models_config.json`
2. Ensure the provider is supported (openai, claude, gemini, grok)
3. Restart the application

### Supported Providers
- **OpenAI**: GPT-4, GPT-4 Turbo, O1, O3-mini
- **Anthropic**: Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku
- **Google**: Gemini 2.0 Flash, Gemini 1.5 Pro
- **xAI**: Grok 2 Latest

## 📊 Features Comparison

| Feature | Original (`main.py`) | Modular (`main_modular.py`) |
|---------|---------------------|----------------------------|
| Basic comparison | ✅ | ✅ |
| Parallel execution | ✅ | ✅ |
| Token statistics | ✅ | ✅ |
| Progress indicators | ❌ | ✅ |
| Summary analytics | ❌ | ✅ |
| Error validation | Basic | Comprehensive |
| Code maintainability | Basic | Excellent |
| Extensibility | Limited | High |

## 🔧 Development

### Architecture Benefits
- **Modularity**: Each component has a single responsibility
- **Extensibility**: Easy to add new models or features
- **Testability**: Components can be tested independently
- **Maintainability**: Clean interfaces and documentation

### Adding a New Model Provider
1. Create new model class in `models/` extending `BaseModel`
2. Implement `_create_client()` and `_generate_response()` methods
3. Register in `ModelFactory`
4. Update configuration

Example:
```python
# models/new_provider_model.py
from .base import BaseModel, TokenInfo

class NewProviderModel(BaseModel):
    def _create_client(self):
        return NewProviderClient()
    
    def _generate_response(self, prompt: str):
        # Implementation here
        pass
```

## 🐛 Troubleshooting

### Common Issues
- **Configuration errors**: Check `models_config.json` syntax
- **API key issues**: Verify environment variables are set
- **Import errors**: Ensure all dependencies are installed
- **Model failures**: Check API key permissions and quotas

### Debug Mode
Run with debug logging:
```bash
streamlit run main_modular.py --logger.level=debug
```

## 📈 Performance Notes
- **Parallel execution** reduces total response time significantly
- **Client reuse** improves efficiency for multiple requests
- **Token usage tracking** helps monitor API costs
- **Error handling** ensures graceful degradation

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License
MIT License - see LICENSE file for details

## 🔗 Links
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [Google Gemini API](https://ai.google.dev/)
- [xAI Grok API](https://docs.x.ai/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**⭐ If you find this tool useful, please consider giving it a star!** 