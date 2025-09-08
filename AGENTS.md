# AGENTS.md — Build & Maintenance Guidance for Coding Agents

## Purpose
This file gives coding agents precise, non-human-facing instructions so they can modify this repo safely without bloating the README.

## Project Summary
A production-ready Streamlit app that compares two LLMs via `any-llm`, reports latency and outputs, and exports Markdown/JSON reports. Features Mock Mode for immediate demo, supports latest models (GPT-5, Claude Sonnet 4), and includes model-specific parameter handling. Prioritize developer experience, clarity, and safe secret handling.

## Current Status
✅ **COMPLETE** - All core functionality implemented and tested
- Mock Mode with realistic model-specific variations
- Real API support for OpenAI, Anthropic, Google, Mistral, OpenRouter
- Latest model support including GPT-5 and Claude Sonnet 4
- Model-specific parameter handling (e.g., GPT-5 temperature requirements)
- Professional README with dual setup options (Demo vs Real API)
- Comprehensive error handling and graceful fallbacks
- Export functionality for Markdown and JSON reports

## Guardrails
- Do NOT introduce a separate backend or database.
- Do NOT add auth or external UI frameworks.
- Keep secrets server-side via environment variables; never expose in the browser.
- If a provider key is missing, disable that provider and show a friendly message.
- Keep total Python code terse and readable; avoid premature abstraction.

## File Contracts
- `app.py`: Streamlit UI + orchestrates calls to `anybench/bench.py`. Provides buttons and shows results. Exposes "Export report". Includes session state management for prompt input and sample button functionality.
- `anybench/bench.py`:
  - `run_once(model_id: str, task: str, prompt: str, mock_mode: bool = False) -> dict`  
    Returns `{ "model": str, "latency_ms": int, "tokens_in": int|None, "tokens_out": int|None, "cost": str|None, "output": str, "ok": bool, "error": str|None }`
  - `run_comparison(model1: str, model2: str, task: str, prompt: str, mock_mode: bool = False) -> dict`
  - `_get_mock_result()` - Generates realistic mock responses with model-specific variations
  - Handles model-specific parameters (e.g., GPT-5 temperature requirements)
- `anybench/tasks.py`:
  - `build_prompt(task: str, user_input: str) -> list[dict]` returning OpenAI-style messages.
  - `get_available_tasks() -> list[str]` - Returns ["summarize", "extract_fields"]
  - `get_task_description(task: str) -> str` - Human-readable task descriptions
- `anybench/providers.py`:
  - `enabled_models() -> list[str]` based on env keys.
  - `get_enabled_providers() -> dict[str, bool]` - Provider availability check
  - `get_default_models() -> list[str]` - Sensible defaults prioritizing latest models
  - `has_any_provider() -> bool` - Check if any providers are available
  - `PROVIDER_MODELS` - Curated model lists with latest versions (GPT-5, Claude Sonnet 4, etc.)
- `anybench/report.py`:
  - `write_markdown(path: str, context: dict) -> None`
  - `write_json(path: str, context: dict) -> None`
  - `export_report(context: dict, base_dir: str = "runs") -> dict[str, str]` - Returns file paths
  - `generate_report_filename(timestamp: str) -> str` - Filesystem-safe naming

## Env & Keys
Expected env vars:
- `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `MISTRAL_API_KEY`, `OPENROUTER_API_KEY`
Behavior:
- If none present → show "No providers enabled" banner and enable Mock Mode.
- Never print secrets to logs. `.env` is gitignored.

## Dependencies & Installation
- `requirements.txt`: streamlit, python-dotenv (any-llm commented out)
- Real API access requires: `pip install "any-llm-sdk[openai,anthropic,google,mistral,openrouter]"`
- Virtual environment recommended: `python -m venv venv && source venv/bin/activate`

## Model Support & Configuration
**Current Model List:**
- **OpenAI:** gpt-5, gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo
- **Anthropic:** claude-3-5-haiku-20241022, claude-3-7-sonnet-20250219, claude-sonnet-4-20250514, claude-opus-4-20250514
- **Google:** gemini-1.5-flash, gemini-1.5-pro
- **Mistral:** mistral-small-latest, mistral-medium-latest
- **OpenRouter:** meta-llama/llama-3.1-8b-instruct:free, google/gemini-pro-1.5

**Model-Specific Handling:**
- GPT-5: No temperature parameter (uses default 1)
- Other models: temperature=0.1 for consistency
- Mock Mode: Realistic variations per model type (OpenAI vs Anthropic vs Google)

## Implementation Status
✅ **COMPLETED TASKS:**
1. ✅ App starts with `streamlit run app.py` and renders sidebar controls
2. ✅ `enabled_models()` returns curated list filtered by available keys
3. ✅ `run_once()` times calls and returns structured metrics
4. ✅ Two tasks implemented: `summarize`, `extract_fields` (JSON)
5. ✅ Report writers implemented; files appear under `runs/`
6. ✅ Graceful error paths and friendly UI messages
7. ✅ Mock Mode with realistic model-specific variations
8. ✅ Model-specific parameter handling (GPT-5 temperature)
9. ✅ Latest model support (GPT-5, Claude Sonnet 4)
10. ✅ Professional README with dual setup options
11. ✅ Session state management for UI interactions
12. ✅ Sample prompt functionality

## Future Enhancement Opportunities
- Add more task types (translation, code generation, etc.)
- Implement model performance scoring/ranking
- Add batch comparison capabilities
- Integrate with any-agent for agent-based comparisons
- Add model cost optimization suggestions
- Implement result caching for repeated comparisons

## Tests (lightweight)
- Manual: with one key present, run comparison and export report. Verify files.
- Manual: with no keys, app starts and shows guidance; Mock Mode works.

## Non-Goals
- No FastAPI/React split.
- No persistent storage.
- No complex evaluation metrics beyond simple heuristics.
