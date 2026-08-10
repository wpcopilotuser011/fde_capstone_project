# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.11+ OR Docker
- OpenAI or Anthropic API key

### Method 1: Docker (Fastest) ⭐

```bash
# 1. Navigate to project
cd "Capstone Assignment"

# 2. Create .env file with your API key
cat > .env << 'EOF'
OPENAI_API_KEY=sk-your-actual-key-here
EOF

# 3. Build and run
chmod +x build.sh run.sh
./build.sh
./run.sh

# 4. Open your browser
# http://localhost:8000/docs
```

### Method 2: Python Virtual Environment

```bash
# 1. Navigate to project
cd "Capstone Assignment"

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cat > .env << 'EOF'
OPENAI_API_KEY=sk-your-actual-key-here
EOF

# 5. Create config file
cp config.local.yaml.example config.local.yaml
# Edit config.local.yaml and add your API key

# 6. Run the application
python -m uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

# 7. Open your browser
# http://localhost:8000/docs
```

## 🎯 Try the AI Features

### 1. Complete Workflow Demo

```bash
curl -X POST http://localhost:8000/api/v1/demo/process-referral
```

This demonstrates all 4 AI opportunities in one call!

### 2. Document Code Extraction (AI Opportunity #1)

```bash
curl -X POST http://localhost:8000/api/v1/documents/analyze \
  -H "Content-Type: application/json" \
  -d '{"document_id": "DOC123", "analysis_type": "full"}'
```

### 3. Specialist Recommendation (AI Opportunity #2)

```bash
curl -X POST http://localhost:8000/api/v1/specialists/search \
  -H "Content-Type: application/json" \
  -d '{
    "specialty": "Cardiology",
    "diagnosis_codes": ["I10"],
    "insurance_provider": "Blue Cross"
  }'
```

### 4. Conversational Assistant (AI Opportunity #6)

```bash
curl -X POST http://localhost:8000/api/v1/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "PT001",
    "message": "What is the status of my referral?"
  }'
```

### 4. Missing Documents Check (AI Opportunity #4)

```bash
curl -X POST "http://localhost:8000/api/v1/documents/check-completeness?specialty=Cardiology" \
  -H "Content-Type: application/json" \
  -d '{"documents": ["referral_form"]}'
```

## 📊 Interactive API Documentation

Open your browser and navigate to:

```
http://localhost:8000/docs
```

You can:
- ✅ See all API endpoints
- ✅ Try them interactively
- ✅ View request/response schemas
- ✅ Test the complete workflow

## 🧪 Run Tests

```bash
# Install test dependencies (if not already)
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=src --cov-report=html
```

## 📖 Documentation

- **README.md** - Complete project documentation
- **API_EXAMPLES.md** - API usage examples
- **ARCHITECTURE.md** - System architecture
- **DEPLOYMENT.md** - Deployment guide for Tekstac VM
- **requirements.md** - Project requirements

## 🔧 Configuration

### Minimal Configuration (Quick Start)

Just create `.env`:
```env
OPENAI_API_KEY=your-key-here
```

### Full Configuration (Production)

Create `config.local.yaml`:
```yaml
ai:
  llm_model: "gpt-4"
  api_key: "your-key-here"
  temperature: 0.7

app:
  environment: "production"
  port: 8000

external_systems:
  mock_mode: true
```

## 🐛 Troubleshooting

### Application won't start

```bash
# Check Python version
python --version  # Should be 3.11+

# Check if port is available
lsof -i :8000  # On Linux/Mac
# Kill process if needed
```

### API key errors

```bash
# Verify .env file exists
cat .env

# Verify it's loaded
# Check logs for "AI agents initialized successfully"
```

### Docker issues

```bash
# Check Docker is running
docker ps

# View logs
docker-compose logs -f

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 🎓 Next Steps

1. **Explore API Docs**: http://localhost:8000/docs
2. **Try the Demo**: `curl -X POST http://localhost:8000/api/v1/demo/process-referral`
3. **Submit Your Own Referral**: Use the `/api/v1/referrals` endpoint
4. **Test AI Features**: Try each of the 4 AI opportunities
5. **Review Architecture**: Read ARCHITECTURE.md
6. **Run Tests**: `pytest tests/ -v`

## 📞 Need Help?

- Check **README.md** for complete documentation
- View **API_EXAMPLES.md** for code samples
- See **DEPLOYMENT.md** for VM deployment
- Check logs: `logs/application.log`
- Verify health: `curl http://localhost:8000/health`

## 🎉 You're Ready!

The platform is now running with:
- ✅ 4 AI opportunities implemented
- ✅ MCP integration for AI agents
- ✅ Complete referral workflow
- ✅ Mock external systems
- ✅ REST API with documentation
- ✅ Docker deployment
- ✅ Test coverage

Start exploring at **http://localhost:8000/docs**! 🚀
