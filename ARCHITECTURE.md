# Architecture Documentation

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
