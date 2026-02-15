#!/usr/bin/env python3
"""Check which configured models are valid and discover new available models."""

import os
import re
import sys
from collections import defaultdict
from config.settings import ConfigManager


PROVIDER_ENV_VARS = {
    "openai": "OPENAI_API_KEY",
    "claude": "ANTHROPIC_API_KEY",
    "gemini": "GOOGLE_API_KEY",
    "grok": "XAI_API_KEY",
}


def fetch_openai_models():
    from openai import OpenAI
    client = OpenAI()
    return [m.id for m in client.models.list().data]


def fetch_claude_models():
    import httpx
    api_key = os.getenv("ANTHROPIC_API_KEY")
    resp = httpx.get(
        "https://api.anthropic.com/v1/models",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        timeout=15,
    )
    resp.raise_for_status()
    return [m["id"] for m in resp.json()["data"]]


def fetch_gemini_models():
    from google import genai
    client = genai.Client()
    return [m.name.removeprefix("models/") for m in client.models.list()]


def fetch_grok_models():
    from openai import OpenAI
    client = OpenAI(
        api_key=os.getenv("XAI_API_KEY"),
        base_url="https://api.x.ai/v1",
    )
    return [m.id for m in client.models.list().data]


FETCHERS = {
    "openai": fetch_openai_models,
    "claude": fetch_claude_models,
    "gemini": fetch_gemini_models,
    "grok": fetch_grok_models,
}


def is_chat_model(provider, model_id):
    """Filter to only chat/text generation models, skipping embeddings, TTS, etc."""
    if provider == "openai":
        if re.search(r"(realtime|audio|tts|transcribe|image|codex)", model_id):
            return False
        return bool(re.match(r"(gpt|o[134])", model_id))
    if provider == "gemini":
        return "gemini" in model_id
    # Anthropic and Grok: show all
    return True


def check_provider(provider, configured_ids, available_ids):
    """Print status for a single provider."""
    available_set = set(available_ids)
    configured_set = set(configured_ids)

    # Configured models: valid or not found
    for mid in configured_ids:
        if mid in available_set:
            print(f"  \033[32m✓\033[0m {mid} (in config)")
        else:
            print(f"  \033[31m✗\033[0m {mid} (NOT FOUND - may be deprecated)")

    # New models not in config
    new_models = sorted(
        mid for mid in available_ids
        if mid not in configured_set and is_chat_model(provider, mid)
    )
    for mid in new_models:
        print(f"  \033[33m+\033[0m {mid} (available, not in config)")


def main():
    config = ConfigManager()
    models_by_provider = defaultdict(list)
    for m in config.models:
        models_by_provider[m.provider].append(m.model_id)

    providers = list(PROVIDER_ENV_VARS.keys())

    for provider in providers:
        print(f"\n=== {provider.capitalize()} ===")

        env_var = PROVIDER_ENV_VARS[provider]
        if not os.getenv(env_var):
            print(f"  (skipped - {env_var} not set)")
            continue

        try:
            available = FETCHERS[provider]()
        except Exception as e:
            print(f"  (error fetching models: {e})")
            continue

        configured = models_by_provider.get(provider, [])
        check_provider(provider, configured, available)

    print()


if __name__ == "__main__":
    main()
