"""Task templates and prompt builders for any-llm Bench."""

from typing import List, Dict


def build_prompt(task: str, user_input: str) -> List[Dict[str, str]]:
    """Build OpenAI-style messages for the given task and user input."""
    
    if task == "summarize":
        return [
            {
                "role": "system",
                "content": "You are a helpful assistant that creates concise, accurate summaries. Focus on the key points and main ideas."
            },
            {
                "role": "user", 
                "content": f"Please summarize the following text:\n\n{user_input}"
            }
        ]
    
    elif task == "extract_fields":
        return [
            {
                "role": "system",
                "content": "You are a helpful assistant that extracts structured data from text. Always respond with valid JSON in the exact format requested."
            },
            {
                "role": "user",
                "content": f"""Extract the following fields from the text below and return them as JSON with keys: vendor, total, date.

If any field is not found, use null for that field.

Text to analyze:
{user_input}

Return only valid JSON in this format:
{{"vendor": "string or null", "total": "number or null", "date": "string or null"}}"""
            }
        ]
    
    else:
        # Fallback for unknown tasks
        return [
            {
                "role": "user",
                "content": user_input
            }
        ]


def get_available_tasks() -> List[str]:
    """Return list of available task types."""
    return ["summarize", "extract_fields"]


def get_task_description(task: str) -> str:
    """Get human-readable description for a task."""
    descriptions = {
        "summarize": "Create a concise summary of the input text",
        "extract_fields": "Extract vendor, total, and date fields as JSON"
    }
    return descriptions.get(task, "Custom task")
