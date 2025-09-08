# any-llm Model Comparator (demo)

A tiny Streamlit app that runs the same prompt against two LLMs via [any-llm] and shows side-by-side outputs and latency. Designed as a developer-onboarding demo: quick to run, easy to extend, and safe with secrets.

## Why this exists
any-llm unifies provider SDKs behind a single interface and normalizes responses to the OpenAI standard. This demo *shows that in action* so developers can compare models transparently and make informed trade-offs.

## Quickstart
```bash
git clone https://github.com/westonludeke/any-llm-bench
cd any-llm-bench
cp env.example .env           # add any keys you have
pip install -r requirements.txt
streamlit run app.py
```

## Configure providers

Add any of these to `.env`:

```
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
MISTRAL_API_KEY=
OPENROUTER_API_KEY=
```

On startup the app enables only providers with keys present. If none are set, you'll see a banner and Mock Mode.

## Using the app

1. Pick two models from the sidebar.
2. Choose a task (Summarize or Extract fields) and enter or paste text.
3. Click **Run comparison** to see outputs + latency.
4. Click **Export report** to save Markdown and JSON under `runs/`.

## Reports

* Markdown: includes models, task, prompt snippet, metrics table, and both outputs.
* JSON: same data for automation or CI.

## Notes & limits

* Token and cost info are best-effort (N/A if unavailable).
* Results are non-deterministic; each run is timestamped.
* Secrets never leave the server process; keys are not stored client-side.

## Stretch ideas

* Add an "Agent toggle" using `any-agent` to show framework overhead.
* Package this as a Blueprint template.
