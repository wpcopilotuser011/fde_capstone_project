# Technical Q&A Preparation

Anticipated questions from a technical review/demo, grouped by topic, with
concise answers grounded in the actual codebase. Use alongside
[DEMO_GUIDE.md](DEMO_GUIDE.md).

## Table of Contents

- [Solution & Requirements](#solution--requirements)
- [Architecture](#architecture)
- [Agents](#agents)
- [MCP](#mcp)
- [LangGraph](#langgraph)
- [Testing & Quality](#testing--quality)
- [Deployment](#deployment)

## Solution & Requirements

**Q: Which AI opportunities did you implement, and why these four?**
A: Extract diagnosis/procedure codes (#1), recommend specialists (#2),
summarize referral history (#3), and identify missing documents (#4) — plus
a bonus conversational assistant (#6). These map directly to the highest
manual-effort, highest-error points in a referral: reading unstructured
clinical documents, matching patients to the right specialist, and
preparing specialists with relevant history before a visit.

**Q: What's mocked vs. real in this implementation?**
A: The LLM call pattern, MCP tool contracts, workflow orchestration, API
layer, database layer, and tests are real and functional. The actual code
extraction/specialist data/eligibility/scheduling responses are mocked
(deterministic sample data) so the demo runs without external
dependencies or live API keys — but every mock sits behind the same
function/tool signature a real LLM or system integration would use, so
swapping in real logic doesn't change any calling code.

## Architecture

**Q: Why FastAPI over Flask/Django?**
A: Native async support (needed for awaiting agent workflows and MCP calls),
automatic OpenAPI docs, and Pydantic-based request/response validation. See
ADR-001 in [ARCHITECTURE.md](../architecture/ARCHITECTURE.md).

**Q: Why SQLite instead of Postgres?**
A: Simple, zero-dependency deployment for the demo; `DatabaseManager` uses
SQLAlchemy so switching to Postgres is a connection-string change, not a
rewrite (ADR-002).

**Q: How are secrets/config handled?**
A: Layered configuration: `config.yaml` (committed, no secrets) →
`config.local.yaml` (gitignored overrides) → `.env` (gitignored secrets) →
environment variables (highest precedence, e.g., in containers).

**Q: How would this scale in production?**
A: Move to Kubernetes, Postgres cluster, Redis cache, a message queue for
async agent processing, and split each MCP server into its own
microservice — outlined under "Scalability Considerations" in
[ARCHITECTURE.md](../architecture/ARCHITECTURE.md).

## Agents

**Q: What's the difference between `ReferralAgent` and
`ConversationalAgentOrchestrator`?**
A: `ReferralAgent` is a LangGraph `StateGraph` that runs a deterministic,
multi-step business workflow once per referral. `ConversationalAgentOrchestrator`
manages open-ended, multi-turn chat sessions (session IDs, history) and
delegates language understanding to the Conversational Assistant MCP tools.
One is a workflow engine; the other is a session/dialogue manager.

**Q: Why doesn't the agent call an LLM to decide the next step (ReAct-style)?**
A: For a regulated healthcare workflow, we want the *sequence* of business
steps to be deterministic and auditable (documents → eligibility →
specialist → scheduling → notification). The LLM/AI is used for *judgment
within* a step (ranking specialists, extracting codes), not for deciding
which step runs next. This is a conscious architecture trade-off between
flexibility and predictability/compliance.

**Q: How do agents call MCP tools today, and how would that change in
production?**
A: In the current reference implementation, each agent node contains an
inline call that mirrors what the MCP tool would return (to keep the demo
runnable without a live MCP client wired in). In production, that inline
call is replaced with an actual MCP client call (`await mcp_client.call_tool("extract_medical_codes", {...})`)
against the running `document_processor`/`specialist_recommender`/`conversational_assistant`
servers — the node logic and state shape don't change.

## MCP

**Q: What is MCP, in one sentence?**
A: A standard protocol for exposing typed, discoverable "tools" that any
compatible AI client or agent can list and call, decoupling tool
implementation from the agent that uses it.

**Q: Why two different MCP implementations (`src/mcp_servers/*` vs.
`src/mcp_server.py`)?**
A: `src/mcp_servers/*` uses the official low-level MCP Python SDK
(`mcp.server.Server`, manual `list_tools`/`call_tool` handlers) — this is
the protocol-accurate reference implementation, useful with any MCP client
(e.g., Claude Desktop). `src/mcp_server.py` uses `FastMCP` with
`@mcp.tool` decorators for a much smaller, faster-to-deploy server, which is
what's targeted at the Tekstac Horizon FastMCP hosting platform.

**Q: How do you test an MCP tool in isolation?**
A: Tools are plain functions/async functions with typed signatures — call
them directly in a unit test (see `tests/test_referral_service.py` for the
equivalent pattern at the service layer) without needing a running agent or
MCP transport.

**Q: How would you secure an MCP server in production?**
A: Transport-level auth (API keys/OAuth on the MCP transport), input
validation on every tool (already partially done via typed parameters),
rate limiting, and running each MCP server in its own least-privilege
container/service boundary rather than a shared process.

## LangGraph

**Q: Walk me through the graph.**
A: `analyze_documents → check_completeness →` (conditional: `continue` →
`verify_eligibility → recommend_specialist → schedule_appointment →
send_notifications → END`, or `request_documents → END`). Full diagram in
[LANGGRAPH_ORCHESTRATION.md](../agents/LANGGRAPH_ORCHESTRATION.md).

**Q: What triggers the conditional branch?**
A: `should_continue_after_docs(state)` checks `state["missing_documents"]`;
if non-empty, the graph routes straight to `END` instead of continuing to
eligibility/specialist/scheduling steps, avoiding wasted work on an
incomplete referral.

**Q: How is state shared between nodes?**
A: A single `ReferralState` `TypedDict` is threaded through every node.
Each node returns the (mutated) state dict; LangGraph merges it back into
the graph's running state (last-write-wins per key, the default reducer
behavior since no custom reducers are defined).

**Q: How would you add error handling/retries to the graph?**
A: The state already has an `errors: List[str]` field reserved for this. A
node would append to it on failure, and a conditional edge (mirroring
`should_continue_after_docs`) would route to a dedicated
`handle_error`/retry node instead of the happy path.

**Q: How would you visualize/debug the graph in production?**
A: LangGraph supports exporting the compiled graph structure (e.g., via
`get_graph().draw_mermaid()`) and integrates with LangSmith for step-by-step
tracing of state transitions and LLM/tool calls — useful for both debugging
and compliance audit trails.

## Testing & Quality

**Q: What's your test coverage strategy?**
A: Unit tests for service-layer business logic (`tests/test_referral_service.py`),
integration tests for API endpoints (`tests/test_api.py`), and a scripted
end-to-end smoke test (`test_all.sh`) that exercises all 4 AI opportunities
plus the full referral workflow.

**Q: How do you validate inputs at the API boundary?**
A: Pydantic models (`src/models.py`) enforce request/response schemas at the
FastAPI layer; MCP tool signatures provide the equivalent typed contract at
the tool-call boundary.

## Deployment

**Q: How is this containerized?**
A: A single `Dockerfile` builds the app image; `docker-compose.yml`
orchestrates it with mounted volumes for `data/` (SQLite DB) and `logs/`,
and reads `config.local.yaml`/`.env` for environment-specific settings. See
[DEPLOYMENT.md](../deployment/DEPLOYMENT.md) for the full Tekstac VM deployment steps.

**Q: What's the difference between the FastAPI deployment and the Horizon
FastMCP deployment?**
A: Same underlying business logic (services layer), two different front
ends: FastAPI (`src/app.py.backup`) exposes REST endpoints for a full web
client; the FastMCP server (`src/app.py`, `src/mcp_server.py`) exposes the
four AI capabilities directly as MCP tools for hosting on Horizon, which
expects a module-level `app`/`mcp` object.
