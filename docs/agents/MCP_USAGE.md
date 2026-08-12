# MCP (Model Context Protocol) Usage

This document explains how MCP is used in the platform, the two different
implementation styles present in the repo, the tools each server exposes,
and how to run/inspect them independently for a demo.

## Table of Contents

- [Why MCP](#why-mcp)
- [Two MCP Implementation Styles in This Repo](#two-mcp-implementation-styles-in-this-repo)
- [MCP Servers and Tools](#mcp-servers-and-tools)
  - [1. Document Processor](#1-document-processor--srcmcp_serversdocument_processorpy)
  - [2. Specialist Recommender](#2-specialist-recommender--srcmcp_serversspecialist_recommenderpy)
  - [3. Conversational Assistant](#3-conversational-assistant--srcmcp_serversconversational_assistantpy)
  - [4. Consolidated FastMCP server](#4-consolidated-fastmcp-server--srcmcp_serverpy--srcapppy)
- [Running the MCP Servers](#running-the-mcp-servers)
  - [stdio reference servers (for MCP-native clients)](#stdio-reference-servers-for-mcp-native-clients)
  - [FastMCP server (Horizon / demo)](#fastmcp-server-horizon--demo)
- [Demonstrating MCP Live](#demonstrating-mcp-live)
- [Key Technical Talking Points](#key-technical-talking-points)

## Why MCP

MCP standardizes how an AI agent or LLM client discovers and calls external
"tools" (functions with typed inputs/outputs). Using MCP instead of ad-hoc
function calling gives us:

- A consistent tool-discovery contract (`list_tools`) any MCP-compatible
  client (Claude Desktop, an IDE, a custom LangGraph node, Horizon) can use.
- Clean separation between **orchestration** (LangGraph agent, decides
  *when* to call a tool) and **capability** (MCP server, implements *what*
  the tool does).
- Independent scaling/deployment: each MCP server can become its own
  microservice without touching agent code.

## Two MCP Implementation Styles in This Repo

| Style | Files | SDK | Use Case |
|-------|-------|-----|----------|
| **stdio MCP servers** (protocol reference implementation) | [src/mcp_servers/document_processor.py](../../src/mcp_servers/document_processor.py), [src/mcp_servers/specialist_recommender.py](../../src/mcp_servers/specialist_recommender.py), [src/mcp_servers/conversational_assistant.py](../../src/mcp_servers/conversational_assistant.py) | `mcp.server.Server` + `@app.list_tools()` / `@app.call_tool()` | Matches the official MCP Python SDK; run over stdio for use with MCP clients like Claude Desktop |
| **FastMCP server** (deployment target) | [src/mcp_server.py](../../src/mcp_server.py), [src/app.py](../../src/app.py) | `fastmcp.FastMCP` with `@mcp.tool` decorators | Simplified single-file server designed to be deployed on the Tekstac **Horizon FastMCP** platform |

Both expose functionally equivalent tools; the `fastmcp`-based version
trades some structure for a much smaller footprint (`@mcp.tool` instead of
manual `list_tools`/`call_tool` handlers) and is what gets deployed for the
live demo/Horizon environment. `src/app.py.backup` preserves the original
FastAPI REST app that fronts the same business logic via HTTP for local
development and testing.

## MCP Servers and Tools

### 1. Document Processor — `src/mcp_servers/document_processor.py`

| Tool | AI Opportunity | Description |
|------|-----------------|-------------|
| `extract_medical_codes` | #1 | Extracts ICD-10 diagnosis codes and CPT procedure codes from clinical text, with confidence scores |
| `check_document_completeness` | #4 | Compares submitted documents against a per-specialty required list and returns missing items + completeness score |

### 2. Specialist Recommender — `src/mcp_servers/specialist_recommender.py`

| Tool | AI Opportunity | Description |
|------|-----------------|-------------|
| `recommend_specialists` | #2 | Ranks specialists by specialty match, insurance network, distance, availability, and rating; returns scored recommendations with human-readable reasons |
| `suggest_alternative_providers` | #2 (bonus) | Provides fallback providers when the top match is unavailable or out-of-network |

### 3. Conversational Assistant — `src/mcp_servers/conversational_assistant.py`

| Tool | AI Opportunity | Description |
|------|-----------------|-------------|
| `handle_patient_query` | #6 | Detects intent (status check, scheduling, specialist search, document help, insurance question, general help) and generates a contextual reply + suggestions |
| `summarize_patient_history` | #3 | Produces a specialist-ready summary of a patient's referral history, conditions, and outcomes |

### 4. Consolidated FastMCP server — `src/mcp_server.py` / `src/app.py`

Exposes all four capabilities plus a convenience end-to-end tool in one
process:

| Tool | Maps to |
|------|---------|
| `extract_medical_codes` | Document Processor AI #1 |
| `recommend_specialists` | Specialist Recommender AI #2 |
| `summarize_patient_history` | Conversational Assistant AI #3 |
| `check_document_completeness` | Document Processor AI #4 |
| `process_referral_workflow` | Runs the whole referral pipeline in one call — useful for demos and health checks |

## Running the MCP Servers

### stdio reference servers (for MCP-native clients)

```bash
python -m src.mcp_servers.document_processor
python -m src.mcp_servers.specialist_recommender
python -m src.mcp_servers.conversational_assistant
```

Point any MCP client (e.g., Claude Desktop's `mcp` config, or a custom
LangChain MCP adapter) at these as stdio servers to list and call tools
interactively.

### FastMCP server (Horizon / demo)

```bash
python -m src.mcp_server
# or, since app.py exposes the same server:
python -m src.app
```

`mcp.run()` starts the server; Horizon (or any FastMCP-compatible host)
expects the module to export a variable named `app` or `mcp` — both are
provided for compatibility.

## Demonstrating MCP Live

1. **List tools** — show `list_tools()` (stdio servers) or the FastMCP tool
   registry to prove the server advertises typed, discoverable tools rather
   than hard-coded endpoints.
2. **Call a tool directly**, bypassing the agent, to show tools are
   independently testable/usable:
   ```python
   from src.mcp_server import extract_medical_codes
   extract_medical_codes("Patient has CAD, ordered ECG", "clinical_note")
   ```
3. **Call the same capability through the agent** (`ReferralAgent`) to show
   how LangGraph nodes invoke these tools as part of a larger workflow — the
   tool implementation doesn't change, only who calls it.
4. Explain the migration path: stdio MCP servers → containerized
   microservices, each independently deployable and versioned, while the
   FastMCP variant is the fastest path to a hosted, callable endpoint for
   Horizon.

## Key Technical Talking Points

- MCP tools are pure functions with typed signatures — easy to unit test in
  isolation (see [tests/test_referral_service.py](../../tests/test_referral_service.py) for the equivalent service-layer tests).
- Confidence scores and structured outputs (not free-text) make MCP tool
  results directly consumable by both the agent and the REST API without
  additional parsing.
- All example data (specialists, codes, patient history) is intentionally
  mocked for the demo; in production each tool would call a real LLM
  (GPT-4/Claude) or external system while keeping the exact same MCP tool
  signature — a key reason MCP is valuable here: swapping the implementation
  behind a tool doesn't require any agent or client changes.
