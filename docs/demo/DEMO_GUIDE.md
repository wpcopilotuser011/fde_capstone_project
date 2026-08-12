# Solution Demonstration Guide

A step-by-step script for presenting this project end-to-end: solution
overview, architecture, agents, MCP usage, and LangGraph orchestration —
followed by a live walkthrough you can run during a demo or review.

## Table of Contents

- [1. Solution Overview (2 minutes)](#1-solution-overview-2-minutes)
- [2. Architecture (3–5 minutes)](#2-architecture-35-minutes)
- [3. Agents (3–5 minutes)](#3-agents-35-minutes)
- [4. MCP Usage (3–5 minutes)](#4-mcp-usage-35-minutes)
- [5. LangGraph Orchestration (3–5 minutes)](#5-langgraph-orchestration-35-minutes)
- [6. Live Walkthrough Commands](#6-live-walkthrough-commands)
  - [Start the API (FastAPI reference implementation)](#start-the-api-fastapi-reference-implementation)
  - [Or run the zero-dependency demo server](#or-run-the-zero-dependency-demo-server)
  - [Exercise each AI opportunity](#exercise-each-ai-opportunity)
  - [Run the test suite as evidence](#run-the-test-suite-as-evidence)
- [7. Closing Summary](#7-closing-summary)

## 1. Solution Overview (2 minutes)

**Elevator pitch:** An AI-powered referral management platform that
automates the healthcare specialist-referral journey — from document intake
to appointment booking — using a LangGraph multi-agent orchestrator backed
by MCP tool servers for AI capabilities.

**4 AI opportunities implemented:**

| # | Capability | Where |
|---|------------|-------|
| 1 | Extract diagnosis/procedure codes from documents | `document_processor` MCP tool `extract_medical_codes` |
| 2 | Recommend specialists (specialty, network, distance, rating) | `specialist_recommender` MCP tool `recommend_specialists` |
| 3 | Summarize patient/referral history for specialists | `conversational_assistant` MCP tool `summarize_patient_history` |
| 4 | Identify missing documents before submission | `document_processor` MCP tool `check_document_completeness` |
| bonus | Conversational assistant for patient queries | `conversational_assistant` MCP tool `handle_patient_query` |

See [PROJECT_SUMMARY.md](../project/PROJECT_SUMMARY.md) for the full requirements
traceability.

## 2. Architecture (3–5 minutes)

Walk through the layered diagram in [ARCHITECTURE.md](../architecture/ARCHITECTURE.md):

```
Client → FastAPI API layer → LangGraph agent orchestration →
MCP tool servers → Service layer → Database → (mock) External systems
```

Highlight:
- Stateless API layer (`src/app.py.backup`, the FastAPI reference app)
- Config layering: `config.yaml` → `config.local.yaml` (gitignored) → `.env`
  → environment variables
- Two deployment targets: full FastAPI service (local/dev) vs. a
  lightweight FastMCP server (`src/app.py`, `src/mcp_server.py`) for Horizon

## 3. Agents (3–5 minutes)

Reference: [AGENTS.md](../agents/AGENTS.md)

- `ReferralAgent` — LangGraph state-machine orchestrator for the referral
  workflow.
- `ConversationalAgentOrchestrator` — session/turn manager for the
  conversational assistant.
- Emphasize the **agent vs. tool** split: agents decide *when*, MCP tools
  implement *what*.

## 4. MCP Usage (3–5 minutes)

Reference: [MCP_USAGE.md](../agents/MCP_USAGE.md)

- Show the three stdio MCP servers under `src/mcp_servers/` (protocol
  reference implementation, `mcp.server.Server` + `list_tools`/`call_tool`).
- Show the consolidated FastMCP server (`src/mcp_server.py`) used for the
  Horizon deployment, exposing the same 4 capabilities plus
  `process_referral_workflow` as a single-call demo tool.
- Call a tool directly (bypassing the agent) to prove it's independently
  testable, then call it via the agent to show reuse.

## 5. LangGraph Orchestration (3–5 minutes)

Reference: [LANGGRAPH_ORCHESTRATION.md](../agents/LANGGRAPH_ORCHESTRATION.md)

- Show the `ReferralState` TypedDict.
- Walk the graph: `analyze_documents → check_completeness → [conditional] →
  verify_eligibility → recommend_specialist → schedule_appointment →
  send_notifications → END`.
- Run the happy path and the "missing documents" early-exit path live.

## 6. Live Walkthrough Commands

### Start the API (FastAPI reference implementation)

```bash
python -m venv venv
venv\Scripts\activate            # Windows
pip install -r requirements.txt
python -m uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000/docs for interactive OpenAPI docs.

### Or run the zero-dependency demo server

```bash
python demo_server.py
```

Then hit the endpoints listed at `GET /docs` (health, referrals, document
analysis, specialist search, history summary, conversation).

### Exercise each AI opportunity

```bash
# AI #1 — extract codes
curl -X POST http://localhost:8000/api/v1/documents/analyze -d @referral_payload.json -H "Content-Type: application/json"

# AI #2 — recommend specialists
curl -X POST http://localhost:8000/api/v1/specialists/search -d '{"specialty":"Cardiology","insurance_provider":"Blue Cross"}' -H "Content-Type: application/json"

# AI #3 — summarize history
curl http://localhost:8000/api/v1/patients/PT001/history

# AI #4 — completeness check
curl -X POST http://localhost:8000/api/v1/documents/check-completeness -d '{"referral_type":"cardiology","documents":[...]}' -H "Content-Type: application/json"

# End-to-end demo workflow
curl -X POST http://localhost:8000/api/v1/demo/process-referral
```

See [API_EXAMPLES.md](../api/API_EXAMPLES.md) and [TEST_PAYLOADS.md](../api/TEST_PAYLOADS.md)
for full request/response bodies.

### Run the test suite as evidence

```bash
pytest tests/test_referral_service.py -v   # unit tests
pytest tests/test_api.py -v                # integration tests
./test_all.sh                              # full scripted demo
```

## 7. Closing Summary

Recap in one sentence per topic:

- **Solution**: automates referral intake → eligibility → specialist match →
  scheduling, using AI where it adds the most value.
- **Architecture**: layered, stateless, config-driven, container-ready.
- **Agents**: LangGraph orchestrator + conversational session manager.
- **MCP usage**: 3 domain MCP servers (stdio) + 1 consolidated FastMCP
  server (Horizon), each independently callable and testable.
- **LangGraph orchestration**: typed state graph with one conditional
  branch, fully auditable via `completed_steps`/`messages`.

Then open the floor for technical questions — see
[TECHNICAL_QA.md](TECHNICAL_QA.md) for prepared answers.
