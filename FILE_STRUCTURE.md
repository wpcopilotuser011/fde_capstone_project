# Project File Structure

## Complete File Tree

```
Capstone Assignment/
│
├── 📋 Documentation Files
│   ├── requirements.md              # Exact project requirements
│   ├── README.md                    # Main project documentation
│   ├── QUICKSTART.md                # 5-minute setup guide
│   ├── API_EXAMPLES.md              # API usage examples
│   ├── ARCHITECTURE.md              # System architecture & design
│   ├── DEPLOYMENT.md                # VM deployment guide
│   ├── TESTING.md                   # Testing procedures
│   └── PROJECT_SUMMARY.md           # Project completion summary
│
├── 🐳 Docker & Deployment
│   ├── Dockerfile                   # Docker image definition
│   ├── docker-compose.yml           # Container orchestration
│   ├── build.sh                     # Build script
│   └── run.sh                       # Run script
│
├── ⚙️ Configuration
│   ├── config.yaml                  # Base configuration (committed)
│   ├── config.local.yaml.example    # Local config template
│   ├── .env.example                 # Environment variables template
│   ├── .gitignore                   # Git ignore rules
│   └── requirements.txt             # Python dependencies
│
├── 💻 Source Code (src/)
│   ├── __init__.py                  # Package init
│   ├── app.py                       # Main FastAPI application ⭐
│   ├── config.py                    # Configuration manager
│   ├── models.py                    # Pydantic data models
│   ├── database.py                  # Database layer
│   │
│   ├── 🤖 agents/                   # AI Agent Orchestration
│   │   ├── __init__.py
│   │   └── referral_agent.py        # LangGraph multi-agent system
│   │
│   ├── 🔌 mcp_servers/              # MCP Server Implementations
│   │   ├── __init__.py
│   │   ├── document_processor.py    # AI Opportunities #1, #4
│   │   ├── specialist_recommender.py # AI Opportunity #2
│   │   └── conversational_assistant.py # AI Opportunities #3, #6
│   │
│   └── 🏪 services/                 # Business Logic Layer
│       ├── __init__.py
│       └── referral_service.py      # Core services
│
├── 🧪 Tests (tests/)
│   ├── __init__.py
│   ├── test_referral_service.py     # Unit tests
│   ├── test_api.py                  # Integration tests
│   └── ../test_all.sh              # Comprehensive test script
│
└── 📁 Runtime Directories (created at runtime)
    ├── data/                        # Database & uploads
    │   ├── referrals.db
    │   └── uploads/
    └── logs/                        # Application logs
        ├── application.log
        └── audit.log
```

## File Count Summary

- **Documentation**: 8 files
- **Configuration**: 5 files
- **Source Code**: 11 Python files
- **Tests**: 3 Python files + 1 shell script
- **Deployment**: 4 files
- **Total**: 32+ files

## Key Files by Purpose

### 🚀 Getting Started
1. **QUICKSTART.md** - Start here!
2. **README.md** - Complete documentation
3. **requirements.md** - Project requirements

### 🔧 Setup & Configuration
1. **.env.example** → create `.env` with your API keys
2. **config.local.yaml.example** → create `config.local.yaml`
3. **requirements.txt** - Install with `pip install -r requirements.txt`

### 🐳 Deployment
1. **build.sh** - Build Docker image
2. **run.sh** - Run container
3. **docker-compose.yml** - Container orchestration

### 💻 Core Application
1. **src/app.py** - Main FastAPI application (entry point)
2. **src/agents/referral_agent.py** - AI orchestration
3. **src/mcp_servers/** - 3 MCP servers for AI capabilities
4. **src/services/referral_service.py** - Business logic

### 🧪 Testing
1. **test_all.sh** - Quick comprehensive test
2. **tests/test_api.py** - API integration tests
3. **tests/test_referral_service.py** - Service unit tests

### 📖 Learning & Reference
1. **ARCHITECTURE.md** - System design
2. **API_EXAMPLES.md** - API usage examples
3. **DEPLOYMENT.md** - VM deployment guide
4. **TESTING.md** - Testing procedures

## Lines of Code

Approximate breakdown:
- Python code: ~2,500 lines
- Documentation: ~2,000 lines
- Configuration: ~200 lines
- Tests: ~400 lines
- **Total**: ~5,100 lines

## File Descriptions

### Documentation

| File | Description | Size |
|------|-------------|------|
| requirements.md | Exact project requirements from assignment | Large |
| README.md | Complete project documentation with usage | Large |
| QUICKSTART.md | 5-minute setup guide | Medium |
| API_EXAMPLES.md | Comprehensive API examples with curl & Python | Large |
| ARCHITECTURE.md | System architecture, design decisions, ADRs | Large |
| DEPLOYMENT.md | Step-by-step VM deployment guide | Large |
| TESTING.md | Testing procedures and guidelines | Large |
| PROJECT_SUMMARY.md | Project completion summary | Medium |

### Configuration

| File | Purpose | Committed |
|------|---------|-----------|
| config.yaml | Base configuration | ✅ Yes |
| config.local.yaml.example | Local config template | ✅ Yes |
| .env.example | Environment variables template | ✅ Yes |
| .gitignore | Git ignore rules | ✅ Yes |
| requirements.txt | Python dependencies | ✅ Yes |

**Note**: `.env` and `config.local.yaml` are created locally (gitignored)

### Source Code

| File | Purpose | AI Opportunity |
|------|---------|----------------|
| app.py | Main FastAPI application | - |
| config.py | Configuration management | - |
| models.py | Pydantic data models | - |
| database.py | Database layer (SQLAlchemy) | - |
| agents/referral_agent.py | LangGraph multi-agent orchestration | All |
| mcp_servers/document_processor.py | Extract codes, check documents | #1, #4 |
| mcp_servers/specialist_recommender.py | Recommend specialists | #2 |
| mcp_servers/conversational_assistant.py | Chat, history summary | #3, #6 |
| services/referral_service.py | Business logic layer | - |

### Tests

| File | Type | Coverage |
|------|------|----------|
| test_referral_service.py | Unit tests | Services |
| test_api.py | Integration tests | API endpoints |
| test_all.sh | Comprehensive test | All features |

### Deployment

| File | Purpose |
|------|---------|
| Dockerfile | Docker image definition |
| docker-compose.yml | Container orchestration |
| build.sh | Build automation script |
| run.sh | Run automation script |

## Important Notes

### Files to Create Locally (Gitignored)

These files must be created on each deployment:

1. **`.env`** - Copy from `.env.example` and add your API keys
2. **`config.local.yaml`** - Copy from `config.local.yaml.example` and configure

### Files Created at Runtime

These directories/files are created automatically:

- `data/` - Database and uploads
- `logs/` - Application and audit logs
- `data/referrals.db` - SQLite database
- `data/uploads/` - Uploaded documents

## Quick Reference

### To Start Development
1. Create `.env` from `.env.example`
2. Run `pip install -r requirements.txt`
3. Run `python -m uvicorn src.app:app --reload`

### To Deploy with Docker
1. Create `.env` with API keys
2. Run `./build.sh`
3. Run `./run.sh`

### To Test
1. Run `./test_all.sh` for quick test
2. Run `pytest tests/` for complete tests

### To Access
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Demo: `curl -X POST http://localhost:8000/api/v1/demo/process-referral`
