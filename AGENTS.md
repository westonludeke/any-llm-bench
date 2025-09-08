# AGENTS.md — Build & Maintenance Guidance for Coding Agents

## Purpose
This file gives coding agents precise, non-human-facing instructions so they can modify this repo safely without bloating the README.

## Project Summary
A tiny Streamlit app that compares two LLMs via `any-llm`, reports latency and outputs, and exports Markdown/JSON reports. Prioritize developer experience, clarity, and safe secret handling.

## Guardrails
- Do NOT introduce a separate backend or database.
- Do NOT add auth or external UI frameworks.
- Keep secrets server-side via environment variables; never expose in the browser.
- If a provider key is missing, disable that provider and show a friendly message.
- Keep total Python code terse and readable; avoid premature abstraction.

## File Contracts
- `app.py`: Streamlit UI + orchestrates calls to `anybench/bench.py`. Provides buttons and shows results. Exposes "Export report".
- `anybench/bench.py`:
  - `run_once(model_id: str, task: str, prompt: str) -> dict`  
    Returns `{ "model": str, "latency_ms": int, "tokens_in": int|None, "tokens_out": int|None, "cost": str|None, "output": str, "ok": bool, "error": str|None }`
- `anybench/tasks.py`:
  - `build_prompt(task: str, user_input: str) -> list[dict]` returning OpenAI-style messages.
- `anybench/providers.py`:
  - `enabled_models() -> list[str]` based on env keys.
- `anybench/report.py`:
  - `write_markdown(path: str, context: dict) -> None`
  - `write_json(path: str, context: dict) -> None`

## Env & Keys
Expected env vars:
- `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `MISTRAL_API_KEY`, `OPENROUTER_API_KEY`
Behavior:
- If none present → show "No providers enabled" banner and enable Mock Mode.
- Never print secrets to logs. `.env` is gitignored.

## Tasks for Agents
1. Ensure app starts with `streamlit run app.py` and renders sidebar controls.
2. Implement `enabled_models()` returning a curated list filtered by available keys.
3. Implement `run_once()` timing the call and returning structured metrics.
4. Implement two tasks: `summarize`, `extract_fields` (JSON).
5. Implement report writers; confirm files appear under `runs/`.
6. Add graceful error paths and friendly UI messages.

## Tests (lightweight)
- Manual: with one key present, run comparison and export report. Verify files.
- Manual: with no keys, app starts and shows guidance; Mock Mode works.

## Non-Goals
- No FastAPI/React split.
- No persistent storage.
- No complex evaluation metrics beyond simple heuristics.
