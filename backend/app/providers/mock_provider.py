from __future__ import annotations

import time


def generate(prompt: str, use_case: str, system_instruction: str) -> dict:
    start = time.perf_counter()
    output = (
        f"[Mock provider] {use_case}: simulated response for prompt '{prompt[:96]}'. "
        "Use this output for UI verification, routing tests, and offline workflows."
    )
    latency_ms = int((time.perf_counter() - start) * 1000) + 28
    return {
        "provider": "Mock",
        "model": "mock-deterministic",
        "status": "Healthy",
        "latency_ms": latency_ms,
        "output": output,
        "note": "Deterministic fallback used for local and offline execution.",
    }

