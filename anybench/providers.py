"""Provider detection and model registry for any-llm Bench."""

import os
from typing import List, Dict


# Curated model lists for each provider
PROVIDER_MODELS = {
    "openai": [
        "openai:gpt-4o-mini",
        "openai:gpt-4o",
        "openai:gpt-3.5-turbo",
    ],
    "anthropic": [
        "anthropic:claude-3-haiku",
        "anthropic:claude-3-sonnet",
        "anthropic:claude-3-opus",
    ],
    "google": [
        "google:gemini-1.5-flash",
        "google:gemini-1.5-pro",
    ],
    "mistral": [
        "mistral:mistral-small-latest",
        "mistral:mistral-medium-latest",
    ],
    "openrouter": [
        "openrouter:meta-llama/llama-3.1-8b-instruct:free",
        "openrouter:google/gemini-pro-1.5",
    ],
}


def get_enabled_providers() -> Dict[str, bool]:
    """Check which providers have API keys available."""
    env_keys = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY", 
        "google": "GOOGLE_API_KEY",
        "mistral": "MISTRAL_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
    }
    
    enabled = {}
    for provider, key_name in env_keys.items():
        enabled[provider] = bool(os.getenv(key_name))
    
    return enabled


def enabled_models() -> List[str]:
    """Return list of available models based on enabled providers."""
    enabled_providers = get_enabled_providers()
    models = []
    
    for provider, is_enabled in enabled_providers.items():
        if is_enabled and provider in PROVIDER_MODELS:
            models.extend(PROVIDER_MODELS[provider])
    
    return models


def has_any_provider() -> bool:
    """Check if at least one provider is enabled."""
    return any(get_enabled_providers().values())


def get_default_models() -> List[str]:
    """Get sensible default models, preferring cheaper/faster options."""
    enabled = enabled_models()
    
    # Prefer these models if available
    preferred = [
        "openai:gpt-4o-mini",
        "anthropic:claude-3-haiku",
        "google:gemini-1.5-flash",
    ]
    
    defaults = []
    for model in preferred:
        if model in enabled:
            defaults.append(model)
            if len(defaults) >= 2:
                break
    
    # If we don't have 2 preferred models, add any others
    for model in enabled:
        if model not in defaults and len(defaults) < 2:
            defaults.append(model)
    
    return defaults
