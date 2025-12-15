"""Lightweight GPT caller for the Codex engine."""

import os


def call_llm(prompt_final: str, model_name: str) -> str:
    """Call the OpenAI Chat Completion API and return the generated text."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

    try:
        from openai import OpenAI  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover - import guard
        raise RuntimeError("openai package is required to call the LLM.") from exc

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt_final}],
    )
    return response.choices[0].message.content or ""
