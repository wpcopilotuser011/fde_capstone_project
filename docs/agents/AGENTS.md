# AI Agents Documentation

This document describes every AI agent in the platform: what it does, how it is
built, what state it owns, and how it fits into the wider system. Use this as
the reference when demonstrating "the agents" part of the solution.

## Table of Contents

- [Agent Inventory](#agent-inventory)
- [1. `ReferralAgent` (Primary Orchestrator)](#1-referralagent-primary-orchestrator)
  - [Construction](#construction)
  - [Agent Steps (Nodes)](#agent-steps-nodes)
  - [Decision Point](#decision-point)
  - [Entry Point](#entry-point)
- [2. `ConversationalAgentOrchestrator`](#2-conversationalagentorchestrator)
- [Agent Design Principles Demonstrated](#agent-design-principles-demonstrated)
- [How Agents Are Invoked From the API](#how-agents-are-invoked-from-the-api)
- [Talking Points for a Live Demo](#talking-points-for-a-live-demo)

## Agent Inventory

| Agent | File | Framework | Purpose |
|-------|------|-----------|---------|
| `ReferralAgent` | [src/agents/referral_agent.py](../../src/agents/referral_agent.py) | LangGraph + LangChain (`ChatOpenAI`) | Orchestrates the end-to-end referral workflow as a state graph |
| `ConversationalAgentOrchestrator` | [src/agents/referral_agent.py](../../src/agents/referral_agent.py) | LangChain-style session orchestrator | Manages multi-turn conversational sessions for the patient-facing assistant |
| Document Processor tools | [src/mcp_servers/document_processor.py](../../src/mcp_servers/document_processor.py) | MCP tool server | Code-extraction and completeness-checking "skills" invoked by `ReferralAgent` |
| Specialist Recommender tools | [src/mcp_servers/specialist_recommender.py](../../src/mcp_servers/specialist_recommender.py) | MCP tool server | Specialist matching "skills" invoked by `ReferralAgent` |
| Conversational Assistant tools | [src/mcp_servers/conversational_assistant.py](../../src/mcp_servers/conversational_assistant.py) | MCP tool server | Intent detection, query handling, and history summarization "skills" |

The design follows a common **agent + tools** pattern: the LangGraph agent is
the "brain" that decides *what* to do next and in *what order*; the MCP
servers are the "hands" that expose callable tools the agent (or any other
MCP-compatible client) can invoke.

## 1. `ReferralAgent` (Primary Orchestrator)

**Responsibility:** Drive a single referral from intake to notification by
executing a deterministic sequence of steps, with one conditional branch.

### Construction

```python
ReferralAgent(model_name="gpt-4", api_key=..., api_base=...)
```

- Wraps `ChatOpenAI` so the same agent code works against OpenAI or an
  OpenAI-compatible endpoint (e.g., Amazon Bedrock access point via
  `api_base`).
- Builds and compiles a `StateGraph` once in `__init__` (`self.workflow`).

### Agent Steps (Nodes)

Each node is an `async def` method that receives the current `ReferralState`,
mutates it, and returns it:

1. **`analyze_documents`** — calls out to the Document Processor MCP tool
   (`extract_medical_codes`) to pull ICD-10/CPT codes out of uploaded
   documents. *(AI Opportunity #1)*
2. **`check_completeness`** — calls the Document Processor MCP tool
   (`check_document_completeness`) to see if required documents are missing.
   *(AI Opportunity #4)*
3. **`verify_eligibility`** — calls the mock payer system to confirm
   insurance eligibility and copay.
4. **`recommend_specialist`** — calls the Specialist Recommender MCP tool
   (`recommend_specialists`) to rank providers. *(AI Opportunity #2)*
5. **`schedule_appointment`** — calls the mock scheduling system to book a
   slot with the selected specialist.
6. **`send_notifications`** — finalizes the workflow and notifies the
   patient/provider.

### Decision Point

```python
def should_continue_after_docs(state) -> str:
    return "request_documents" if state.get("missing_documents") else "continue"
```

If documents are incomplete, the graph short-circuits straight to `END`
instead of proceeding to eligibility/specialist steps — this is the one
conditional edge in the graph (see [LANGGRAPH_ORCHESTRATION.md](LANGGRAPH_ORCHESTRATION.md)
for the full graph diagram).

### Entry Point

```python
await referral_agent.process_referral({
    "referral_id": "REF001",
    "patient_id": "PT001",
    "documents": [...]
})
```

Internally this seeds a `ReferralState`, invokes `self.workflow.ainvoke(state)`,
and returns the final state (all extracted codes, eligibility result,
recommended specialist, appointment, and the running message transcript).

## 2. `ConversationalAgentOrchestrator`

**Responsibility:** Own multi-turn conversational sessions (session IDs,
turn history) and delegate actual language understanding to the
Conversational Assistant MCP tools.

- `handle_conversation(user_id, message, session_id=None)` creates a session
  if one doesn't exist, then returns an assistant reply, detected intent, and
  follow-up suggestions.
- Session state is deliberately lightweight in this reference
  implementation (in-memory dict); production would back this with Redis or
  a database table so sessions survive restarts and scale across replicas.

## Agent Design Principles Demonstrated

- **Separation of orchestration vs. skills** — the LangGraph agent contains
  no domain logic; every domain capability (code extraction, specialist
  matching, completeness checks, conversation) is implemented as an MCP tool
  and merely *called* by the agent. This makes tools reusable outside the
  agent (e.g., directly from the FastAPI layer or another agent).
- **Typed state** — `ReferralState` is a `TypedDict`, so every node has a
  clear contract for what it reads and writes. This avoids "stringly typed"
  state bugs common in ad-hoc agent loops.
- **Explicit control flow** — instead of letting an LLM freely decide the
  next tool call (a ReAct-style loop), the workflow graph encodes the
  *business process* explicitly. The LLM/tools are used for judgement within
  a step (e.g., ranking specialists), not for deciding the overall sequence.
  This is intentional for a regulated healthcare workflow where auditability
  matters.
- **Message trail as audit log** — every node appends an `AIMessage` to
  `state["messages"]`, giving a natural-language audit trail of what the
  agent did and why, in addition to the structured `completed_steps` list.

## How Agents Are Invoked From the API

`src/app.py.backup` (the FastAPI reference implementation) wires the agent
into request handling via `BackgroundTasks`, so a client submitting a
referral gets an immediate `202`-style response with a `referral_id`, while
`ReferralAgent.process_referral(...)` continues running the workflow
asynchronously. The demo/Horizon deployment (`src/app.py`, `src/mcp_server.py`)
exposes the same underlying capabilities directly as MCP tools for simpler,
stateless invocation — see [MCP_USAGE.md](MCP_USAGE.md).

## Talking Points for a Live Demo

1. Show `ReferralState` and explain it is the single source of truth passed
   between nodes — no hidden global state.
2. Trigger a referral with an incomplete document set and show the graph
   short-circuiting via `should_continue_after_docs`.
3. Trigger a referral with a complete document set and walk through the
   `completed_steps` and `messages` in the final state to narrate the whole
   journey.
4. Explain why orchestration (LangGraph) and skills (MCP) are split into two
   layers — reusability, testability, and clear audit boundaries.
