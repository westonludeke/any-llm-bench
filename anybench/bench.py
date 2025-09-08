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
    """Generate mock results for demo purposes with model-specific variations."""
    
    # Determine model characteristics for more realistic mock data
    if "gpt" in model_id.lower() or "openai" in model_id.lower():
        model_type = "openai"
        base_latency = 120
        base_cost = "$0.0001"
    elif "claude" in model_id.lower() or "anthropic" in model_id.lower():
        model_type = "anthropic"
        base_latency = 180
        base_cost = "$0.0002"
    elif "gemini" in model_id.lower() or "google" in model_id.lower():
        model_type = "google"
        base_latency = 140
        base_cost = "$0.0001"
    else:
        model_type = "generic"
        base_latency = 150
        base_cost = "$0.0001"
    
    # Generate task-specific outputs with model variations
    if task == "summarize":
        if model_type == "openai":
            output = f"**Summary:** The provided text ({len(prompt)} characters) contains key information that can be distilled into main points. The content appears to cover important topics that would benefit from a structured overview highlighting the most significant elements."
        elif model_type == "anthropic":
            output = f"Here's a concise summary of the {len(prompt)}-character text: The material presents several key concepts and details that are relevant to the main topic. The most important points include the primary themes and supporting information that provide context and depth to the subject matter."
        else:
            output = f"This is a mock summary of the input text. The original text was approximately {len(prompt)} characters long and contained various information that would typically be summarized here."
    
    elif task == "extract_fields":
        if model_type == "openai":
            output = '{"vendor": "Acme Corporation", "total": 1250.00, "date": "2024-01-15"}'
        elif model_type == "anthropic":
            output = '{"vendor": "Tech Solutions Inc", "total": 987.50, "date": "2024-01-20"}'
        else:
            output = '{"vendor": "Mock Vendor Inc", "total": 123.45, "date": "2024-01-15"}'
    
    else:
        output = f"Mock response for {task} task with input length {len(prompt)} characters."
    
    # Add some variation to metrics
    import random
    latency_variation = random.randint(-20, 20)
    token_variation = random.randint(-5, 5)
    
    return {
        "model": f"{model_id} (Mock)",
        "latency_ms": max(50, base_latency + latency_variation),
        "tokens_in": int(len(prompt.split()) * 1.3) + token_variation,
        "tokens_out": int(len(output.split()) * 1.3) + token_variation,
        "cost": base_cost,
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
