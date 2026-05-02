# Sentinella Product Blueprint

## 1. One-Line Pitch

Sentinella is an AI reliability and guardrails platform that helps teams monitor model behavior, compare providers, review traces, and control routing policies from one engineering workspace.

## 2. Why This Product

This is a strong second AI product direction because it gives:

- a horizontal AI engineering platform rather than another vertical app
- direct LLMOps and observability relevance
- strong discussion points around cost, latency, safety, and fallback logic
- room for multi-provider orchestration and evaluation
- a clear complement to Convivio without repeating the same workflow

## 3. Users

### AI Platform Lead

- monitors provider quality
- reviews budget and routing policy
- decides model standards

### ML Engineer

- compares outputs
- tests prompt behavior
- tracks evaluation quality

### Applied AI Engineer

- inspects traces
- diagnoses weak or unsafe model responses
- tunes fallback logic

### Safety or Operations Reviewer

- flags problematic responses
- reviews policy violations
- tracks incident trends

## 4. Main Entities

- User
- Provider
- PromptRun
- Trace
- EvaluationRun
- EvaluationResult
- RoutingRule
- IncidentFlag
- PolicyCheck

## 5. Core Screens

- login
- dashboard
- provider registry
- trace explorer
- evaluation board
- routing rules
- playground / live comparison

## 6. Initial Product Scope

### Backend

- demo auth
- provider registry data
- dashboard metrics
- trace listing
- evaluation listing
- routing rule listing
- live compare endpoint with Gemini and mock providers

### Frontend

- engineering workspace shell
- dashboard metrics
- provider cards
- trace review list
- evaluation summaries
- routing rule panel
- compare playground

## 7. Design Direction

Sentinella should feel precise, technical, and calm.

### Visual language

- deep graphite and midnight base
- cyan and ice-blue signals
- amber for warnings
- crimson for incidents
- muted slate surfaces for trace readability

### UI tone

- engineering-first
- dense but clear
- strong status hierarchy
- obvious separation between healthy, warning, and risky states

## 8. Architecture Direction

### Backend

- FastAPI route layer
- service layer for traces, evaluations, and provider calls
- provider abstraction for Gemini and future connectors
- typed schemas for requests and response contracts
- in-memory demo store replaceable with persistence later

### Frontend

- feature-oriented React structure
- API wrapper for authenticated calls
- reusable metric, trace, and provider panels
- comparison playground with explicit provider results

## 9. Engineering Value

- provider abstraction
- live LLM comparison
- operational AI visibility
- cost / latency / reliability thinking
- safer and more mature AI system design discussion

## 10. Future Expansion

- OpenAI, Anthropic, and Ollama support
- prompt registry and version history
- output evaluation scoring
- policy engine and blocklists
- incident review workflows

