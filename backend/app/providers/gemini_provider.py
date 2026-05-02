from __future__ import annotations

import json
import time
from urllib import error, request

from app.core.settings import settings


def is_enabled() -> bool:
    return bool(settings.gemini_api_key)


def generate(prompt: str, use_case: str, system_instruction: str) -> dict:
    if not is_enabled():
        raise RuntimeError("Gemini API key is not configured.")

    endpoint = f"{settings.gemini_api_base}/models/{settings.gemini_model}:generateContent"
    prompt_text = (
        f"{system_instruction.strip()}\n\n"
        f"Use case: {use_case}\n\n"
        f"User prompt:\n{prompt.strip()}\n\n"
        "Respond clearly, professionally, and concisely."
    )
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt_text,
                    }
                ]
            }
        ]
    }

    http_request = request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": settings.gemini_api_key,
        },
        method="POST",
    )

    started = time.perf_counter()
    try:
        with request.urlopen(http_request, timeout=settings.llm_timeout_seconds) as response:
            raw = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gemini request failed with HTTP {exc.code}: {error_body}") from exc
    latency_ms = int((time.perf_counter() - started) * 1000)

    text = raw["candidates"][0]["content"]["parts"][0]["text"]
    return {
        "provider": "Gemini",
        "model": settings.gemini_model,
        "status": "Healthy",
        "latency_ms": latency_ms,
        "output": text.strip(),
        "note": "Live provider comparison through Gemini.",
    }
