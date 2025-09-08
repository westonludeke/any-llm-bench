"""Model execution and benchmarking for any-llm Bench."""

import time
import json
from typing import Dict, Any, Optional
from .tasks import build_prompt

# Try to import any_llm, fall back to mock if not available
try:
    import any_llm
    ANY_LLM_AVAILABLE = True
except ImportError:
    ANY_LLM_AVAILABLE = False
    print("Warning: any-llm not available. Install with: pip install git+https://github.com/mozilla-ai/any-llm.git")


def run_once(model_id: str, task: str, prompt: str, mock_mode: bool = False) -> Dict[str, Any]:
    """
    Run a single model execution and return structured results.
    
    Returns:
        {
            "model": str,
            "latency_ms": int,
            "tokens_in": int|None,
            "tokens_out": int|None, 
            "cost": str|None,
            "output": str,
            "ok": bool,
            "error": str|None
        }
    """
    
    if mock_mode or not ANY_LLM_AVAILABLE:
        return _get_mock_result(model_id, task, prompt)
    
    try:
        # Build the prompt messages
        messages = build_prompt(task, prompt)
        
        # Time the execution
        start_time = time.perf_counter()
        
        # Call any-llm
        response = any_llm.completion(
            model=model_id,
            messages=messages,
            temperature=0.1  # Low temperature for more consistent results
        )
        
        end_time = time.perf_counter()
        latency_ms = int((end_time - start_time) * 1000)
        
        # Extract response data
        output = response.choices[0].message.content if response.choices else ""
        
        # Try to extract token counts and cost if available
        tokens_in = getattr(response.usage, 'prompt_tokens', None) if hasattr(response, 'usage') else None
        tokens_out = getattr(response.usage, 'completion_tokens', None) if hasattr(response, 'usage') else None
        cost = getattr(response, 'cost', None)
        
        # For extract_fields task, validate JSON output
        ok = True
        error = None
        if task == "extract_fields":
            try:
                json.loads(output)
            except json.JSONDecodeError:
                ok = False
                error = "Invalid JSON output"
        
        return {
            "model": model_id,
            "latency_ms": latency_ms,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "cost": str(cost) if cost is not None else None,
            "output": output,
            "ok": ok,
            "error": error
        }
        
    except Exception as e:
        return {
            "model": model_id,
            "latency_ms": 0,
            "tokens_in": None,
            "tokens_out": None,
            "cost": None,
            "output": "",
            "ok": False,
            "error": str(e)
        }


def _get_mock_result(model_id: str, task: str, prompt: str) -> Dict[str, Any]:
    """Generate mock results for demo purposes."""
    
    if task == "summarize":
        output = f"This is a mock summary of the input text. The original text was approximately {len(prompt)} characters long and contained various information that would typically be summarized here."
    elif task == "extract_fields":
        output = '{"vendor": "Mock Vendor Inc", "total": 123.45, "date": "2024-01-15"}'
    else:
        output = f"Mock response for {task} task with input length {len(prompt)} characters."
    
    return {
        "model": f"{model_id} (Mock)",
        "latency_ms": 150,  # Simulated latency
        "tokens_in": len(prompt.split()) * 1.3,  # Rough estimate
        "tokens_out": len(output.split()) * 1.3,
        "cost": "$0.0001",
        "output": output,
        "ok": True,
        "error": None
    }


def run_comparison(model1: str, model2: str, task: str, prompt: str, mock_mode: bool = False) -> Dict[str, Any]:
    """Run comparison between two models and return combined results."""
    
    result1 = run_once(model1, task, prompt, mock_mode)
    result2 = run_once(model2, task, prompt, mock_mode)
    
    return {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "task": task,
        "prompt": prompt,
        "model1": result1,
        "model2": result2,
        "mock_mode": mock_mode
    }
