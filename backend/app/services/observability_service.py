from __future__ import annotations

import logging
from datetime import datetime, timezone
from urllib import error
from uuid import uuid4

from app.api.schemas import CompareRequest
from app.providers import gemini_provider, mock_provider
from app.store import demo_store


logger = logging.getLogger(__name__)


def compare_providers(payload: CompareRequest) -> list[dict]:
    results: list[dict] = []

    for provider_name in payload.providers:
        provider_key = provider_name.lower()

        try:
            if provider_key == "gemini":
                result = gemini_provider.generate(payload.prompt, payload.use_case, payload.system_instruction)
            else:
                result = mock_provider.generate(payload.prompt, payload.use_case, payload.system_instruction)
        except (RuntimeError, error.URLError, TimeoutError, KeyError, IndexError) as exc:
            logger.warning("Provider compare failed for %s: %s", provider_name, exc)
            result = {
                "provider": provider_name.title(),
                "model": "unavailable",
                "status": "Degraded",
                "latency_ms": 0,
                "output": "Provider call failed. Review configuration or fallback policy.",
                "note": str(exc),
            }

        trace = {
            "id": f"trace-{uuid4().hex[:8]}",
            "use_case": payload.use_case,
            "provider": result["provider"],
            "model": result["model"],
            "status": result["status"],
            "latency_ms": result["latency_ms"],
            "risk_level": "Medium" if result["status"] != "Healthy" else "Low",
            "prompt_excerpt": payload.prompt[:180],
            "output_excerpt": result["output"][:180],
            "created_at": datetime.now(timezone.utc),
        }
        demo_store.add_trace(trace)
        results.append(result)

    return results

