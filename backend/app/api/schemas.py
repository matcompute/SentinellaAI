from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class UserDto(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    role: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserDto


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str


class DashboardMetricDto(BaseModel):
    label: str
    value: str
    detail: str
    trend: str


class DashboardHighlightDto(BaseModel):
    id: str
    title: str
    detail: str
    tone: str
    timestamp: datetime


class DashboardResponse(BaseModel):
    metrics: list[DashboardMetricDto]
    highlights: list[DashboardHighlightDto]
    watch_items: list[str]


class ProviderDto(BaseModel):
    id: str
    name: str
    mode: str
    status: str
    avg_latency_ms: int
    success_rate: float
    est_cost_per_1k: str
    note: str


class TraceDto(BaseModel):
    id: str
    use_case: str
    provider: str
    model: str
    status: str
    latency_ms: int
    risk_level: str
    prompt_excerpt: str
    output_excerpt: str
    created_at: datetime


class EvaluationResultDto(BaseModel):
    id: str
    use_case: str
    baseline_provider: str
    challenger_provider: str
    verdict: str
    quality_delta: str
    cost_delta: str
    latency_delta: str
    created_at: datetime


class RoutingRuleDto(BaseModel):
    id: str
    name: str
    priority: int
    condition: str
    action: str
    status: str


class CompareRequest(BaseModel):
    prompt: str = Field(min_length=8, max_length=1500)
    providers: list[str] = Field(min_length=1)
    use_case: str = Field(min_length=3, max_length=120)
    system_instruction: str = Field(default="Provide a concise, high-quality answer.")


class CompareResultDto(BaseModel):
    provider: str
    model: str
    status: str
    latency_ms: int
    output: str
    note: str


class CompareResponse(BaseModel):
    use_case: str
    results: list[CompareResultDto]

