"""Thin OpenAI-compatible chat client. Works with Groq, Ollama, Gemini's OpenAI endpoint, etc."""
import time

from openai import OpenAI, RateLimitError

from .config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not LLM_API_KEY:
            raise RuntimeError("LLM_API_KEY is empty. Set it in .env (free key from console.groq.com).")
        _client = OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)
    return _client


def chat(messages: list[dict], temperature: float = 0.0, retries: int = 4) -> str:
    for attempt in range(retries):
        try:
            resp = _get_client().chat.completions.create(
                model=LLM_MODEL, messages=messages, temperature=temperature
            )
            return resp.choices[0].message.content.strip()
        except RateLimitError:
            # free tiers are rate-limited: back off and retry
            time.sleep(2 ** attempt * 2)
    raise RuntimeError("LLM rate limit: gave up after retries")
