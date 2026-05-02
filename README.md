# Sentinella

Sentinella is an AI reliability and guardrails platform for teams that build LLM applications, agent systems, and model-assisted workflows. It helps engineering teams monitor provider behavior, inspect traces, compare outputs, and enforce routing rules from one operational workspace.

The name comes from the Italian word `sentinella`, meaning sentinel or guard. It fits a product focused on visibility, protection, and control for AI systems in production.

## Product Position

Sentinella is positioned as an AI control-tower product for teams that need reliability, observability, and governance around model usage:

- Python + React full-stack product direction
- multi-provider LLM operations
- traces, evaluations, and routing visibility
- a horizontal engineering platform rather than a business vertical application

## Stack

- Python 3.10+
- FastAPI
- Pydantic
- Uvicorn
- React 18
- Vite 5
- provider abstraction for Gemini and mock mode

## Current Features

- demo-authenticated engineering workspace
- provider registry with health, latency, cost, and success indicators
- trace explorer for model request and output review
- evaluation board for prompt and provider comparisons
- routing rule panel for fallback and safety policies
- prompt playground for live provider comparison
- Gemini provider support with a safe mock fallback

## Demo Accounts

Seeded users are available for local development. Configure `DEMO_PASSWORD` in `backend/.env`, then sign in with one of these accounts:

- `lead@sentinella.io`
- `mlops@sentinella.io`
- `safety@sentinella.io`

## Local Run

Environment:

```powershell
cd backend
Copy-Item .env.example .env
```

Then set:

```env
DEMO_PASSWORD=your_local_demo_password
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3-flash-preview
```

For a local non-billed mode:

```env
LLM_PROVIDER=mock
```

Backend:

```powershell
.\scripts\Run-Backend.ps1
```

Frontend:

```powershell
.\scripts\Run-Frontend.ps1
```

Open:

```text
http://127.0.0.1:4204
```

API health:

```text
http://127.0.0.1:5062/api/health
```

## How It Works

Sentinella is designed around an AI engineering workflow:

1. Connect one or more model providers.
2. Send prompts or trace samples through the playground.
3. Compare outputs, latency, and basic cost signals.
4. Review recent traces for weak answers, safety problems, or provider drift.
5. Track evaluation outcomes over time.
6. Define routing rules for fallback, cost control, or risk handling.

The current version uses seeded operational data for a realistic walkthrough, while the provider comparison flow can call Gemini in real time through the backend provider layer.

## Verification

Backend health:

```powershell
Invoke-RestMethod http://127.0.0.1:5062/api/health
```

Frontend production build:

```powershell
cd frontend
npm run build
```

## Roadmap

- OpenAI, Anthropic, and Ollama provider connectors
- trace tagging and reviewer assignment
- output policy checks and hallucination signals
- prompt version registry and experiment history
- budget guardrails and provider auto-routing
