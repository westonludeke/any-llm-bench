# any-llm Model Comparator (demo)

A tiny Streamlit app that runs the same prompt against two LLMs via [any-llm] and shows side-by-side outputs and latency. Designed as a developer-onboarding demo: quick to run, easy to extend, and safe with secrets.

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

The app will automatically detect no API keys and enable **Mock Mode** - you can test all features immediately with simulated responses!

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
2. Choose a task (Summarize or Extract fields) and enter or paste text.
3. Click **Run comparison** to see outputs + latency.
4. Click **Export report** to save Markdown and JSON under `runs/`.

### Supported Models

**OpenAI:** GPT-5, GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-3.5-turbo  
**Anthropic:** Claude Sonnet 4, Claude 3.7 Sonnet, Claude 3.5 Haiku, Claude Opus 4  
**Google:** Gemini 1.5 Flash, Gemini 1.5 Pro  
**Mistral:** Mistral Small, Mistral Medium  
**OpenRouter:** Various community models

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
