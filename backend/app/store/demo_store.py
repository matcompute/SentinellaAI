from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.core.settings import settings


UTC = timezone.utc

USERS = [
    {
        "id": "usr-lead",
        "full_name": "Elia Rinaldi",
        "email": "lead@sentinella.io",
        "role": "AI Platform Lead",
    },
    {
        "id": "usr-mlops",
        "full_name": "Lucia Moretti",
        "email": "mlops@sentinella.io",
        "role": "MLOps Engineer",
    },
    {
        "id": "usr-safety",
        "full_name": "Paolo Serra",
        "email": "safety@sentinella.io",
        "role": "Safety Reviewer",
    },
]

SESSIONS: dict[str, str] = {}

PROVIDERS = [
    {
        "id": "provider-gemini",
        "name": "Gemini",
        "mode": "Cloud",
        "status": "Healthy",
        "avg_latency_ms": 1640,
        "success_rate": 0.98,
        "est_cost_per_1k": "Low",
        "note": "Fast balanced provider for comparison and default experiments.",
    },
    {
        "id": "provider-mock",
        "name": "Mock",
        "mode": "Local",
        "status": "Healthy",
        "avg_latency_ms": 34,
        "success_rate": 1.0,
        "est_cost_per_1k": "None",
        "note": "Fallback provider for offline development and deterministic demos.",
    },
]

TRACES = [
    {
        "id": "trace-2001",
        "use_case": "Campaign summary safety review",
        "provider": "Gemini",
        "model": "gemini-3-flash-preview",
        "status": "Flagged",
        "latency_ms": 1910,
        "risk_level": "Medium",
        "prompt_excerpt": "Summarize a premium restaurant campaign with urgency but avoid discount language.",
        "output_excerpt": "One response over-used scarcity language and weakened the brand tone.",
        "created_at": datetime.now(UTC) - timedelta(minutes=22),
    },
    {
        "id": "trace-2002",
        "use_case": "Review response drafting",
        "provider": "Gemini",
        "model": "gemini-3-flash-preview",
        "status": "Healthy",
        "latency_ms": 1510,
        "risk_level": "Low",
        "prompt_excerpt": "Draft a reply to a 3-star review with a warm but accountable tone.",
        "output_excerpt": "Response remained concise, acknowledged the issue, and preserved hospitality tone.",
        "created_at": datetime.now(UTC) - timedelta(hours=1, minutes=8),
    },
    {
        "id": "trace-2003",
        "use_case": "Fallback smoke test",
        "provider": "Mock",
        "model": "mock-deterministic",
        "status": "Healthy",
        "latency_ms": 31,
        "risk_level": "Low",
        "prompt_excerpt": "Generate a minimal response for offline verification.",
        "output_excerpt": "Fallback returned predictable structure for UI continuity.",
        "created_at": datetime.now(UTC) - timedelta(hours=2, minutes=41),
    },
]

EVALUATIONS = [
    {
        "id": "eval-301",
        "use_case": "Guest review response quality",
        "baseline_provider": "Mock",
        "challenger_provider": "Gemini",
        "verdict": "Gemini wins",
        "quality_delta": "+32%",
        "cost_delta": "+Low",
        "latency_delta": "+1.5s",
        "created_at": datetime.now(UTC) - timedelta(hours=5),
    },
    {
        "id": "eval-302",
        "use_case": "Campaign summary consistency",
        "baseline_provider": "Gemini",
        "challenger_provider": "Mock",
        "verdict": "Gemini wins",
        "quality_delta": "+44%",
        "cost_delta": "+Low",
        "latency_delta": "+1.6s",
        "created_at": datetime.now(UTC) - timedelta(days=1, hours=1),
    },
]

ROUTING_RULES = [
    {
        "id": "rule-401",
        "name": "Fallback on provider failure",
        "priority": 1,
        "condition": "If primary provider returns an error or times out after 45 seconds",
        "action": "Retry with Mock provider and flag the trace",
        "status": "Active",
    },
    {
        "id": "rule-402",
        "name": "Escalate high-risk outputs",
        "priority": 2,
        "condition": "If output mentions unsupported brand claims or unsafe legal certainty",
        "action": "Flag for reviewer approval before publication",
        "status": "Active",
    },
]


def _safe_user(user: dict) -> dict:
    return dict(user)


def authenticate(email: str, password: str) -> dict | None:
    if password != settings.demo_password:
        return None

    for user in USERS:
        if user["email"].lower() == email.lower():
            return _safe_user(user)
    return None


def create_session(user_id: str) -> str:
    token = f"sentinella-{uuid4().hex}"
    SESSIONS[token] = user_id
    return token


def get_user_by_token(token: str) -> dict | None:
    user_id = SESSIONS.get(token)
    if not user_id:
        return None
    for user in USERS:
        if user["id"] == user_id:
            return _safe_user(user)
    return None


def list_providers() -> list[dict]:
    return deepcopy(PROVIDERS)


def list_traces() -> list[dict]:
    return deepcopy(sorted(TRACES, key=lambda item: item["created_at"], reverse=True))


def list_evaluations() -> list[dict]:
    return deepcopy(sorted(EVALUATIONS, key=lambda item: item["created_at"], reverse=True))


def list_routing_rules() -> list[dict]:
    return deepcopy(sorted(ROUTING_RULES, key=lambda item: item["priority"]))


def add_trace(trace: dict) -> dict:
    TRACES.append(trace)
    return deepcopy(trace)
