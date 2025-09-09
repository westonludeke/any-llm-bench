# any-llm Bench — Side-by-Side Model Comparator

A lightweight Streamlit app that lets you run the same prompt across two LLMs using [any-llm](https://github.com/mozilla-ai/any-llm), with side-by-side outputs and latency metrics. It’s built as a developer-onboarding demo: quick to run, easy to extend, and designed with transparency and safe secret handling in mind.

<img src="https://p52.f0.n0.cdn.zight.com/items/YEuEW9k6/d1beb09c-e7c6-40b3-8582-4d8ea6067198.jpg" width="800">

## Contents
- [Live Demo](#-live-demo)
- [Quickstart](#quickstart)
- [Mock Mode](#mock-mode)
- [Configure Providers](#configure-real-api-providers)
- [Using the App](#using-the-app)
- [Reports](#reports)
- [Key Features](#key-features)
- [Notes & Limits](#notes--limits)
- [Stretch Ideas](#stretch-ideas)
- [Feedback & Contributions](#-feedback--contributions)
- [License](#license)

## 🚀 Live Demo

🎥 **Watch the 5-minute demo video:** [YouTube Link](https://youtu.be/your-link-here)  
💻 **Try it now:** [any-llm-bench.streamlit.app](https://any-llm-bench.streamlit.app)

*This demo runs in Mock Mode: no API keys required*

## Why this exists
any-llm unifies provider SDKs behind a single interface and normalizes responses to the OpenAI standard. This demo *shows that in action* so developers can compare models transparently and make informed trade-offs.

## Quickstart

### Option 1: Demo Mode (No API Keys Required)
```bash
git clone https://github.com/westonludeke/any-llm-bench
cd any-llm-bench

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will automatically detect no API keys and enable **Mock Mode**, you can test all features immediately with simulated responses.

### Option 2: Real API Mode (With API Keys)
```bash
git clone https://github.com/westonludeke/any-llm-bench
cd any-llm-bench

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install "any-llm-sdk[openai,anthropic,google,mistral,openrouter]"  # install any-llm with providers

# Configure API keys
cp env.example .env           # add your API keys

# Run the app
streamlit run app.py
```

## Mock Mode

**Mock Mode** is automatically enabled when no API keys are detected. This feature:

- ✅ **Works immediately** without any setup
- ✅ **Simulates realistic responses** with model-specific variations
- ✅ **Shows different outputs** for different model types (GPT vs Claude vs Gemini)
- ✅ **Includes realistic metrics** (latency, tokens, cost)
- ✅ **Perfect for demos** and testing the interface

Mock Mode demonstrates the complete workflow and is ideal for:
- **Code reviews** and demonstrations
- **Testing the interface** without API costs
- **Understanding the app** before adding real keys

## Configure Real API Providers

Add any of these to your `.env` file:

```
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
GOOGLE_API_KEY=your-google-key-here
MISTRAL_API_KEY=your-mistral-key-here
OPENROUTER_API_KEY=your-openrouter-key-here
```

**Note:** You only need to add keys for providers you want to use. The app automatically detects which providers are available and enables only those models.

## Using the app

1. Pick two models from the sidebar (including latest GPT-5, Claude Sonnet 4, and more).
2. Choose a task and enter or paste text.
3. Click **Run comparison** to see outputs + latency.
4. Click **Export report** to save Markdown and JSON under `runs/`.

### Available Tasks

**📝 Summarize**
- Creates concise, accurate summaries of long text
- Perfect for document analysis and content distillation
- Shows how different models approach summarization
- Ideal for comparing model writing styles and focus areas

**📊 Extract Fields**
- Extracts structured data (vendor, total, date) from text
- Returns results as validated JSON format
- Great for invoice processing and data extraction
- Tests model ability to follow structured output requirements
- Validates JSON output and marks errors if format is invalid

### Supported Models

**OpenAI:** GPT-5, GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-3.5-turbo  
**Anthropic:** Claude Sonnet 4, Claude 3.7 Sonnet, Claude 3.5 Haiku, Claude Opus 4  
**Google:** Gemini 1.5 Flash, Gemini 1.5 Pro  
**Mistral:** Mistral Small, Mistral Medium  
**OpenRouter:** Various community models

### Adding Additional Models

To add new models or providers, edit `anybench/providers.py`:

**Adding a new model to existing provider:**
```python
"google": [
    "google:gemini-1.5-flash",
    "google:gemini-1.5-pro",
    "google:gemini-2.0-flash",  # Add new model here
],
```

**Adding a new provider:**
```python
# 1. Add to PROVIDER_MODELS
"new_provider": [
    "new_provider:model-name",
],

# 2. Add environment variable detection
env_keys = {
    # ... existing providers
    "new_provider": "NEW_PROVIDER_API_KEY",
}
```

**Note:** Ensure the model names match the exact identifiers expected by any-llm and the provider's API.

## Reports

* Markdown: includes models, task, prompt snippet, metrics table, and both outputs.
* JSON: same data for automation or CI.

## Key Features

* **Latest Models:** Support for GPT-5, Claude Sonnet 4, and other cutting-edge models
* **Smart Fallbacks:** Automatic Mock Mode when no API keys are present
* **Model-Specific Handling:** Proper parameter handling for different model requirements
* **Real-time Metrics:** Latency, token usage, and cost tracking
* **Export Functionality:** Markdown and JSON reports for analysis
* **Cross-Provider Comparison:** Side-by-side analysis across different AI providers

## Notes & limits

* Token and cost info are best-effort (N/A if unavailable).
* Results are non-deterministic; each run is timestamped.
* Secrets never leave the server process; keys are not stored client-side.
* GPT-5 uses default temperature (1) - custom temperature not supported.

## Stretch ideas

* Add an "Agent toggle" using `any-agent` to show framework overhead.
* Package this as a Blueprint template.

## 🤝 Feedback & Contributions

**Questions, comments, or feedback?** 
- Open a [GitHub Issue](https://github.com/westonludeke/any-llm-bench/issues) for questions or bug reports
- Suggest new features or improvements
- Share your use cases and experiences

## License

This project is licensed under the [Apache License 2.0](./LICENSE).