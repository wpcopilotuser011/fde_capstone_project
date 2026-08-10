# Deployment Guide for Tekstac Virtual Machine

## Pre-Deployment Checklist

### ✅ Before Copying Code to VM

1. **Test locally first**
   ```bash
   python -m uvicorn src.app:app --reload
   # Verify at http://localhost:8000/docs
   ```

2. **Ensure all secrets are in gitignored files**
   - `.env` file exists with API keys
   - `config.local.yaml` has configuration
   - These files are listed in `.gitignore`

3. **Test Docker build locally**
   ```bash
   ./build.sh
   ./run.sh
   # Verify container runs
   docker-compose logs -f
   ```

## Step 1: Copy Project to Virtual Machine

### Option A: Using SCP (if you have direct access)

```bash
# From your local machine
cd /path/to/parent/directory
scp -r "Capstone Assignment" username@tekstac-vm:/home/username/
```

### Option B: Using Git (recommended)

```bash
# On local machine
cd "Capstone Assignment"
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main

# On VM
git clone <your-repo-url> "Capstone Assignment"
cd "Capstone Assignment"
```

### Option C: Manual Copy (if using web interface)

1. Zip the entire project folder
2. Upload to VM
3. Extract on VM

## Step 2: Setup on Tekstac VM

### 1. Connect to VM

```bash
ssh username@tekstac-vm-address
```

### 2. Navigate to Project

```bash
cd "Capstone Assignment"
```

### 3. Create Configuration Files

**Important:** These files are gitignored, so create them on the VM

```bash
# Create .env file
cat > .env << 'EOF'
OPENAI_API_KEY=your_actual_openai_key_here
ANTHROPIC_API_KEY=your_actual_anthropic_key_here
APP_ENV=production
LOG_LEVEL=INFO
EOF

# Create config.local.yaml
cat > config.local.yaml << 'EOF'
ai:
  llm_model: "gpt-4"
  api_key: "your_actual_openai_key_here"
  temperature: 0.7
  max_tokens: 2000

app:
  environment: "production"
  host: "0.0.0.0"
  port: 8000

external_systems:
  mock_mode: true

logging:
  level: "INFO"
EOF
```

### 4. Verify Python Version

```bash
python --version  # Should be 3.11+
```

If not installed:
```bash
# Follow Tekstac platform instructions for Python installation
```

### 5. Install Docker (if not already installed)

```bash
# Check if Docker is installed
docker --version

# If not installed, follow Tekstac platform instructions
```

## Step 3: Build and Deploy

### Method 1: Using Docker (Recommended for Evaluation)

```bash
# Make scripts executable
chmod +x build.sh run.sh

# Build Docker image
./build.sh

# Run container
./run.sh

# Verify deployment
curl http://localhost:8000/health
```

### Method 2: Using Docker Compose

```bash
# Start services
docker-compose up -d

# Check logs
docker-compose logs -f

# Verify
curl http://localhost:8000/health
```

### Method 3: Direct Python (if Docker not available)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python -m uvicorn src.app:app --host 0.0.0.0 --port 8000
```

## Step 4: Verify Deployment

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "ai_agents": "active"
}
```

### 2. Test API Docs

Open in browser:
```
http://<vm-ip>:8000/docs
```

### 3. Run Demo Workflow

```bash
curl -X POST http://localhost:8000/api/v1/demo/process-referral
```

### 4. Check Logs

```bash
# Docker logs
docker-compose logs -f

# Or application logs
tail -f logs/application.log
```

## Step 5: Run Tests (Optional)

```bash
# If running directly with Python
pytest tests/ -v

# If using Docker
docker-compose exec referral-platform pytest tests/ -v
```

## Troubleshooting

### Issue: Port 8000 already in use

```bash
# Find process using port
sudo lsof -i :8000

# Kill process or change port in config
```

### Issue: Database errors

```bash
# Ensure data directory exists
mkdir -p data logs

# Reset database
rm data/referrals.db
# Restart application
```

### Issue: AI features not working

```bash
# Verify API keys are set
echo $OPENAI_API_KEY

# Check config file
cat config.local.yaml

# View logs for specific errors
tail -100 logs/application.log
```

### Issue: Container won't start

```bash
# Check container status
docker ps -a

# View container logs
docker logs referral-management-platform

# Rebuild image
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Evaluation Checklist

Before evaluation, ensure:

- [ ] Container is running: `docker ps`
- [ ] Health endpoint works: `curl http://localhost:8000/health`
- [ ] API docs accessible: `http://localhost:8000/docs`
- [ ] Demo workflow works: `curl -X POST http://localhost:8000/api/v1/demo/process-referral`
- [ ] All 4 AI opportunities are accessible via API
- [ ] Logs are being written: `ls -lh logs/`
- [ ] Database is created: `ls -lh data/`

## Accessing from Outside VM

If you need to access from your local machine:

```bash
# On VM, expose port (if firewall allows)
# Access using VM's public IP
http://<vm-public-ip>:8000/docs

# Or setup SSH tunnel from local machine
ssh -L 8000:localhost:8000 username@tekstac-vm
# Then access http://localhost:8000 on local machine
```

## Stopping the Application

```bash
# Using docker-compose
docker-compose down

# Remove volumes (caution: deletes data)
docker-compose down -v

# Or kill direct Python process
pkill -f uvicorn
```

## Quick Commands Reference

```bash
# Start
./run.sh

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Check status
docker-compose ps

# Access container shell
docker-compose exec referral-platform /bin/bash

# View app logs
tail -f logs/application.log

# Test endpoint
curl http://localhost:8000/health
```

## FastMCP on Horizon Deployment

If deploying specifically to FastMCP on Horizon:

1. **Follow Horizon-specific instructions** from your platform
2. **Ensure config.local.yaml and .env are properly set** with Horizon credentials
3. **Use the provided Docker setup** - it's Horizon-compatible
4. **Environment variables** can be set in Horizon's config

## Support During Evaluation

If evaluators encounter issues:

1. Check logs: `docker-compose logs -f`
2. Verify health: `curl http://localhost:8000/health`
3. Access interactive docs: `http://localhost:8000/docs`
4. Run demo workflow: `curl -X POST http://localhost:8000/api/v1/demo/process-referral`

All functionality is demonstrated through the REST API and interactive documentation.
