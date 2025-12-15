"""Lightweight GPT caller for the Codex engine."""

import os
from openai import OpenAI


def call_llm(prompt_final: str, model_name: str) -> str:
    """Call the OpenAI Chat Completion API and return the generated text."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt_final}],
    )
    return response.choices[0].message.content or ""
