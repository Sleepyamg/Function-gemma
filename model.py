import time
from typing import Any

import requests

from prompt import build_prompt

OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "gemma3:270m"
MAX_RETRIES = 3
RETRY_BACKOFF_SEC = 0.5


def generate_raw_response(user_request: str, model: str = DEFAULT_MODEL) -> str:
    prompt = build_prompt(user_request)
    payload: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2},
    }
    last_error: Exception | None = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(
                OLLAMA_GENERATE_URL,
                json=payload,
                timeout=120,
            )
            resp.raise_for_status()
            data = resp.json()
            text = data.get("response", "")
            if isinstance(text, str) and text.strip():
                return text
            last_error = RuntimeError("Empty response from Ollama")
        except (requests.RequestException, ValueError, KeyError) as e:
            last_error = e
        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_BACKOFF_SEC * (attempt + 1))
    if last_error:
        raise last_error
    raise RuntimeError("Ollama request failed after retries")
