# any-llm Bench — A side-by-side model comparator demo

any-llm Bench is a lightweight demo app that shows how to run the same prompt across multiple LLMs using [any-llm](https://github.com/mozilla-ai/any-llm).  
It highlights one of any-llm's core strengths — **swap providers with a single string and get standardized results** — while giving developers a transparent way to compare latency, cost, and output style side by side.  

This project is designed as an onboarding example: easy to clone, quick to configure, and useful for understanding both the developer experience and the trade-offs between different model providers.

**You are building a tiny demo app for Mozilla.ai's `any-llm`** to compare LLM outputs across providers. Prioritize developer experience and clarity over features. 

## Goal

A minimal tool that:

1. lets a user enter/select a prompt,
2. runs it against 2 models via `any-llm`,
3. shows side-by-side outputs + latency (and tokens if available),
4. exports a Markdown + JSON report.

## Tech choices 

* Keep it simple

## Secrets & models

* Read provider keys from environment: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `MISTRAL_API_KEY`, `OPENROUTER_API_KEY`.
* On startup, detect which keys are present; only enable those providers.
* Provide two sensible default models (adjust if unavailable):

  * `openai:gpt-4o-mini`
  * `anthropic:claude-3-haiku`
* If neither is available, surface a friendly **"No providers enabled"** banner and offer **Mock Mode** with canned outputs.

## UX requirements

* Left sidebar:

  * Provider/model dropdowns (filter models by enabled providers).
  * Task selector: **Summarize** | **Extract fields**.
  * Optional prompt presets toggle.
* Main pane:

  * Prompt textarea.
  * "Run comparison" button.
  * Results table: model, latency\_ms, tokens\_in?, tokens\_out?, cost? (N/A if unknown).
  * Two expandable panels with raw outputs.
  * "Export report" button → writes `runs/run-<timestamp>.md` and `.json`.
* If a model is selected without its key, show a clear error and do not crash.

## Implementation hints

* `anybench/bench.py`:

  * Use `time.perf_counter()` around the `any_llm.completion` call.
  * Capture output string and any token fields if available; otherwise None.
* `anybench/tasks.py`:

  * `summarize(text)` prompt template.
  * `extract_fields(text)` prompt for JSON output with schema {vendor, total, date}.
  * Add tiny JSON-parse guard for extract task; if invalid, mark as such.
* `anybench/providers.py`:

  * Minimal registry mapping provider availability (from env) to model strings.
  * Provide a small curated list for each provider; fall back gracefully.
* `anybench/report.py`:

  * Markdown report with: timestamp, models, task, prompt snippet, metrics table, and outputs.
  * JSON report mirrors the structure.

## DX polish

* `.env.example` with empty keys.
* `requirements.txt` pinned major versions (`streamlit`, `python-dotenv`, `any-llm`).
* Friendly empty state when no keys present; optional **Mock Mode** constant outputs.
* Log errors succinctly in Streamlit, not to stdout spam.

## Acceptance criteria

* App runs with `streamlit run app.py`.
* With at least one provider key set, user can compare two models and see outputs + latency.
* "Export report" writes both files under `runs/`.
* With no keys, app starts and explains how to add keys, and Mock Mode works.
* Code < \~300 LOC excluding generated files; clear separation per file layout.

Create the project now following these specs.
