from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.api.schemas import (
    CompareRequest,
    CompareResponse,
    CompareResultDto,
    DashboardResponse,
    EvaluationResultDto,
    HealthResponse,
    LoginRequest,
    LoginResponse,
    ProviderDto,
    RoutingRuleDto,
    TraceDto,
    UserDto,
)
from app.core.settings import settings
from app.services.observability_service import compare_providers
from app.store import demo_store


router = APIRouter(prefix=settings.api_prefix)
security = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(security)) -> dict:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required.")

    user = demo_store.get_user_by_token(credentials.credentials)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session is invalid.")

    return user


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="sentinella-api")


@router.post("/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    user = demo_store.authenticate(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

    token = demo_store.create_session(user["id"])
    return LoginResponse(access_token=token, user=UserDto(**user))


@router.get("/auth/me", response_model=UserDto)
def me(user: dict = Depends(get_current_user)) -> UserDto:
    return UserDto(**user)


@router.get("/dashboard", response_model=DashboardResponse)
def dashboard(user: dict = Depends(get_current_user)) -> DashboardResponse:
    providers = demo_store.list_providers()
    traces = demo_store.list_traces()
    evaluations = demo_store.list_evaluations()

    metrics = [
        {
            "label": "Active Providers",
            "value": str(len(providers)),
            "detail": "Connected providers in the control plane",
            "trend": "Gemini + mock live",
        },
        {
            "label": "Recent Traces",
            "value": str(len(traces)),
            "detail": "Stored traces available for review",
            "trend": f"{len([item for item in traces if item['status'] != 'Healthy'])} flagged",
        },
        {
            "label": "Evaluation Runs",
            "value": str(len(evaluations)),
            "detail": "Prompt and provider comparisons tracked",
            "trend": "Weekly regression watch",
        },
        {
            "label": "Healthy Success Rate",
            "value": "98%",
            "detail": "Recent live provider reliability",
            "trend": "Stable",
        },
    ]
    highlights = [
        {
            "id": "hl-1",
            "title": "Gemini remains default comparison path",
            "detail": "Recent evaluation runs continue to favor Gemini quality over the deterministic fallback.",
            "tone": "positive",
            "timestamp": traces[0]["created_at"],
        },
        {
            "id": "hl-2",
            "title": "One flagged campaign summary trace",
            "detail": "A recent output leaned too hard on urgency language and needs prompt review.",
            "tone": "attention",
            "timestamp": traces[0]["created_at"],
        },
    ]
    return DashboardResponse(
        metrics=metrics,
        highlights=highlights,
        watch_items=[
            "Watch provider drift on marketing-heavy prompts",
            "Keep fallback rules explicit for degraded provider states",
            "Track latency spikes before enabling auto-routing",
        ],
    )


@router.get("/providers", response_model=list[ProviderDto])
def providers(user: dict = Depends(get_current_user)) -> list[ProviderDto]:
    return [ProviderDto(**item) for item in demo_store.list_providers()]


@router.get("/traces", response_model=list[TraceDto])
def traces(user: dict = Depends(get_current_user)) -> list[TraceDto]:
    return [TraceDto(**item) for item in demo_store.list_traces()]


@router.get("/evaluations", response_model=list[EvaluationResultDto])
def evaluations(user: dict = Depends(get_current_user)) -> list[EvaluationResultDto]:
    return [EvaluationResultDto(**item) for item in demo_store.list_evaluations()]


@router.get("/routing-rules", response_model=list[RoutingRuleDto])
def routing_rules(user: dict = Depends(get_current_user)) -> list[RoutingRuleDto]:
    return [RoutingRuleDto(**item) for item in demo_store.list_routing_rules()]


@router.post("/playground/compare", response_model=CompareResponse)
def playground_compare(payload: CompareRequest, user: dict = Depends(get_current_user)) -> CompareResponse:
    results = compare_providers(payload)
    return CompareResponse(
        use_case=payload.use_case,
        results=[CompareResultDto(**item) for item in results],
    )

