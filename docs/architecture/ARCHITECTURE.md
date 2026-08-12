# Architecture Documentation

## Table of Contents

- [System Architecture](#system-architecture)
  - [High-Level Architecture](#high-level-architecture)
- [Component Architecture](#component-architecture)
  - [1. API Layer (FastAPI)](#1-api-layer-fastapi)
  - [2. AI Agent Orchestration (LangGraph)](#2-ai-agent-orchestration-langgraph)
  - [3. MCP Servers](#3-mcp-servers)
  - [4. Service Layer](#4-service-layer)
  - [5. Data Layer](#5-data-layer)
- [Data Flow](#data-flow)
  - [Referral Submission Flow](#referral-submission-flow)
- [AI Agent Workflow](#ai-agent-workflow)
  - [LangGraph State Machine](#langgraph-state-machine)
- [Security Architecture](#security-architecture)
  - [Configuration Management](#configuration-management)
  - [Secrets Management](#secrets-management)
  - [Audit Logging](#audit-logging)
- [Deployment Architecture](#deployment-architecture)
  - [Docker Container](#docker-container)
- [Scalability Considerations](#scalability-considerations)
  - [Current Implementation](#current-implementation)
  - [Production Recommendations](#production-recommendations)
- [Non-Functional Requirements](#non-functional-requirements)
  - [Performance](#performance)
  - [Availability](#availability)
  - [Scalability](#scalability-1)
  - [Security](#security)
- [Concepts Implemented in the Current Codebase](#concepts-implemented-in-the-current-codebase)
  - [Application Entrypoints](#application-entrypoints)
  - [AI Agent Orchestration](#ai-agent-orchestration-1)
  - [MCP Tool Servers](#mcp-tool-servers)
  - [Service & Data Layer](#service--data-layer)
  - [Configuration & Secrets](#configuration--secrets)
  - [Testing](#testing)
- [Technology Decisions](#technology-decisions)
  - [ADR-001: FastAPI vs Flask](#adr-001-fastapi-vs-flask)
  - [ADR-002: SQLite vs PostgreSQL](#adr-002-sqlite-vs-postgresql)
  - [ADR-003: LangGraph vs Custom Orchestration](#adr-003-langgraph-vs-custom-orchestration)
  - [ADR-004: MCP Protocol](#adr-004-mcp-protocol)

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
│  (Web UI, Mobile App, Healthcare Provider Portal)               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                           │
│                    FastAPI REST API                              │
│  - Authentication/Authorization                                  │
│  - Request Validation                                            │
│  - Rate Limiting                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   AI Agent Orchestration                         │
│              LangGraph Multi-Agent System                        │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Document    │  │  Specialist  │  │ Conversation │          │
│  │  Processor   │  │  Recommender │  │   Agent      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MCP Server Layer                              │
│              Model Context Protocol Servers                      │
│                                                                   │
│  ┌───────────────────┐  ┌───────────────────┐                   │
│  │ Document MCP      │  │ Specialist MCP    │                   │
│  │ - Extract codes   │  │ - Recommend       │                   │
│  │ - Check docs      │  │ - Alternative     │                   │
│  └───────────────────┘  └───────────────────┘                   │
│                                                                   │
│  ┌───────────────────┐                                           │
│  │ Conversation MCP  │                                           │
│  │ - Handle query    │                                           │
│  │ - Summarize hist  │                                           │
│  └───────────────────┘                                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Business Logic Layer                           │
│                  Service Components                              │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Referral    │  │   Document   │  │   History    │          │
│  │  Service     │  │   Service    │  │   Service    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Data Access Layer                             │
│                  Database Manager                                │
│  - SQLAlchemy ORM                                                │
│  - Connection Pooling                                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Persistence Layer                              │
│                                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │Referrals │  │ Patients │  │Providers │  │Documents │        │
│  │   DB     │  │    DB    │  │    DB    │  │    DB    │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                  External System Integration                     │
│                                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │   EHR    │  │  Payer   │  │Scheduling│  │   Labs   │        │
│  │ Systems  │  │ Systems  │  │ Systems  │  │  Pharm   │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
│     (Mock)         (Mock)         (Mock)        (Mock)          │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. API Layer (FastAPI)

**Responsibilities:**
- RESTful API endpoints
- Request/response validation
- Authentication & authorization
- CORS handling
- Error handling

**Key Files:**
- `src/app.py` - Main FastAPI application

### 2. AI Agent Orchestration (LangGraph)

**Responsibilities:**
- Multi-agent workflow coordination
- State management
- Decision routing
- Agent communication

**Key Files:**
- `src/agents/referral_agent.py` - Main orchestration agent

**Workflow Graph:**
```
Start → Analyze Documents → Check Completeness → 
Verify Eligibility → Recommend Specialist → 
Schedule Appointment → Send Notifications → End
```

### 3. MCP Servers

**Document Processor MCP:**
- Tool: `extract_medical_codes`
- Tool: `check_document_completeness`
- AI Opportunities: #1, #4

**Specialist Recommender MCP:**
- Tool: `recommend_specialists`
- Tool: `suggest_alternative_providers`
- AI Opportunities: #2, #7

**Conversational Assistant MCP:**
- Tool: `handle_patient_query`
- Tool: `summarize_patient_history`
- AI Opportunities: #3, #6

### 4. Service Layer

**Referral Service:**
- Submit referral
- Track status
- Verify eligibility
- Search specialists
- Schedule appointments

**Document Service:**
- Analyze documents
- Extract codes
- Check completeness

**History Service:**
- Generate summaries
- Retrieve patient history

### 5. Data Layer

**Models:**
- Referral
- Patient
- Provider
- Document
- Appointment
- Audit Log

## Data Flow

### Referral Submission Flow

```
1. Client submits referral → API validates request
2. Service creates referral record
3. Background: AI agent starts processing
4. Agent analyzes documents → MCP Document Processor
5. Agent checks completeness → MCP Document Processor
6. Agent verifies eligibility → External Payer API (mock)
7. Agent recommends specialist → MCP Specialist Recommender
8. Agent schedules appointment → External Scheduling API (mock)
9. Agent sends notifications
10. Client receives response with referral ID
```

## AI Agent Workflow

### LangGraph State Machine

```python
State = {
    "referral_id": str,
    "patient_id": str,
    "messages": List[Message],
    "documents": List[Document],
    "diagnosis_codes": List[Code],
    "missing_documents": List[str],
    "eligibility_status": Dict,
    "recommended_specialists": List[Specialist],
    "appointment": Dict,
    "current_step": str,
    "completed_steps": List[str]
}
```

## Security Architecture

### Configuration Management

```
┌─────────────────────────────────────────┐
│          Configuration Sources          │
├─────────────────────────────────────────┤
│  1. config.yaml (base, committed)       │
│  2. config.local.yaml (overrides, git-  │
│     ignored)                             │
│  3. .env (secrets, gitignored)          │
│  4. Environment variables (runtime)     │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│       Configuration Manager              │
│  - Deep merge strategy                   │
│  - Priority: env vars > local > base    │
└─────────────────────────────────────────┘
```

### Secrets Management

- API keys in `.env` file (gitignored)
- Configuration in `config.local.yaml` (gitignored)
- No secrets in code or base config
- Environment-specific overrides

### Audit Logging

- All critical operations logged
- Timestamp, user, action, resource
- Stored in audit_logs table

## Deployment Architecture

### Docker Container

```
┌─────────────────────────────────────────┐
│        Docker Container                  │
│                                          │
│  ┌────────────────────────────────┐     │
│  │  FastAPI Application           │     │
│  │  - Uvicorn ASGI Server         │     │
│  │  - Port 8000                   │     │
│  └────────────────────────────────┘     │
│                                          │
│  ┌────────────────────────────────┐     │
│  │  Application Code              │     │
│  │  - src/                        │     │
│  │  - config.yaml                 │     │
│  └────────────────────────────────┘     │
│                                          │
│  ┌────────────────────────────────┐     │
│  │  Data Volumes (mounted)        │     │
│  │  - /app/data (SQLite DB)       │     │
│  │  - /app/logs (log files)       │     │
│  │  - /app/config.local.yaml      │     │
│  └────────────────────────────────┘     │
└─────────────────────────────────────────┘
```

## Scalability Considerations

### Current Implementation
- Single container deployment
- SQLite database
- Mock external systems

### Production Recommendations
- Multi-container orchestration (Kubernetes)
- PostgreSQL database cluster
- Redis for caching
- Message queue (RabbitMQ/Kafka) for async processing
- Load balancer
- Separate MCP servers as microservices

## Non-Functional Requirements

### Performance
- API response time: < 200ms (p95)
- Document processing: < 5s
- Concurrent users: 100+

### Availability
- Target uptime: 99.9%
- Health checks every 30s
- Auto-restart on failure

### Scalability
- Horizontal scaling ready
- Stateless API design
- Database connection pooling

### Security
- HTTPS in production
- API key authentication
- Input validation
- HIPAA compliance patterns

## Concepts Implemented in the Current Codebase

A concrete snapshot of what is actually built and working today, mapped to files, as
opposed to the aspirational design in [FUTURE_ARCHITECTURE.md](FUTURE_ARCHITECTURE.md).

### Application Entrypoints
- `src/app.py` / `src/mcp_server.py` - **FastMCP** tool server (`FastMCP("Referral-Management")`) exposing MCP tools; this is the active entrypoint.
- `src/app.py.backup` - the original **FastAPI** REST implementation (`/api/v1/referrals`, `/api/v1/eligibility`, `/api/v1/conversation`, etc.). Kept for reference; not the active entrypoint. The "API Layer (FastAPI)" description in [Component Architecture](#1-api-layer-fastapi) reflects this backup file.

### AI Agent Orchestration
- `src/agents/referral_agent.py` - `ReferralAgent` and `ConversationalAgentOrchestrator`, built on **LangGraph** (`StateGraph`, `Graph`, `END`).
- Model selection is fully **environment-driven**: `DEFAULT_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-4")`. No proprietary/real model identifier is hardcoded anywhere in source or committed config - the actual model in use lives only in the gitignored `.env`.
- Uses `langchain_core.messages` and `langchain_openai.ChatOpenAI` as the LLM client.

### MCP Tool Servers
- `src/mcp_servers/document_processor.py` - `extract_medical_codes`, `check_document_completeness`.
- `src/mcp_servers/specialist_recommender.py` - `recommend_specialists`, `suggest_alternative_providers`.
- `src/mcp_servers/conversational_assistant.py` - `handle_patient_query`, `summarize_patient_history`.

### Service & Data Layer
- `src/services/referral_service.py` - business logic for submission, status tracking, eligibility, specialist search, scheduling.
- `src/database.py` - SQLAlchemy models (`ReferralDB`, `PatientDB`, `ProviderDB`, `DocumentDB`, `AppointmentDB`, `AuditLogDB`).
- **Database connectivity with automatic fallback**: `DatabaseManager._create_engine()` reads `DB_TYPE` (default `mysql`), builds a `mysql+pymysql://` URL from `MYSQL_HOST/PORT/USER/PASSWORD/DATABASE` env vars (via `PyMySQL`, credentials URL-encoded with `quote_plus`), and test-connects with a 5s timeout. If MySQL is unreachable for any reason, it transparently falls back to a local SQLite file (`data/referrals.db`) instead of raising - the app never fails to start due to a missing database server.
- No conversation/chat-history persistence table exists yet (LLM conversation state is in-memory only for the life of a process) - this is a known gap addressed conceptually in [FUTURE_ARCHITECTURE.md](FUTURE_ARCHITECTURE.md#7-persistent-session-management).

### Configuration & Secrets
- `src/config.py` - `ConfigManager` merges `config.yaml` (base, committed) → `config.local.yaml` (gitignored overrides) → environment variables, in that priority order.
- Environment-variable overrides implemented today: `LLM_MODEL_NAME` → `ai.llm_model`, `DB_TYPE` → `database.type`, and `MYSQL_HOST` / `MYSQL_PORT` / `MYSQL_USER` / `MYSQL_DATABASE` → `database.mysql.*` (the MySQL password is deliberately excluded from the in-memory config dict and read directly from the environment only, so it never ends up in a config dump or log).
- `.env` holds all secrets (API keys, MySQL password) and is gitignored; `requirements.txt` includes `PyMySQL==1.1.1` and `python-dotenv` to support this.

### Testing
- `tests/test_api.py`, `tests/test_referral_service.py` - unit/integration tests using `pytest`.

## Technology Decisions

### ADR-001: FastAPI vs Flask
**Decision:** FastAPI
**Rationale:**
- Native async support
- Auto-generated OpenAPI docs
- Pydantic validation
- Better performance

### ADR-002: SQLite vs PostgreSQL
**Decision:** SQLite (dev), PostgreSQL-ready
**Rationale:**
- Simple deployment for demo
- Easy migration path
- No external dependencies

### ADR-003: LangGraph vs Custom Orchestration
**Decision:** LangGraph
**Rationale:**
- Built for multi-agent workflows
- State management
- Clear graph visualization
- Industry standard

### ADR-004: MCP Protocol
**Decision:** Implement MCP servers
**Rationale:**
- Requirement for assignment
- Demonstrates AI integration
- Scalable agent architecture
- Industry emerging standard
