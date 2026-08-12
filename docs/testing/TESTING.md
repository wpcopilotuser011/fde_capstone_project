# Testing Guide

## Table of Contents

- [Overview](#overview)
- [Test Coverage](#test-coverage)
  - [Unit Tests](#unit-tests)
  - [Integration Tests](#integration-tests)
  - [AI Opportunity Tests](#ai-opportunity-tests)
- [Running Tests](#running-tests)
  - [Quick Test (All Features)](#quick-test-all-features)
  - [Unit Tests](#unit-tests-1)
  - [Integration Tests](#integration-tests-1)
  - [All Tests with Coverage](#all-tests-with-coverage)
- [Manual Testing](#manual-testing)
  - [Using Interactive API Docs](#using-interactive-api-docs)
  - [Using cURL](#using-curl)
  - [Using Python](#using-python)
- [Test Data](#test-data)
  - [Sample Patients](#sample-patients)
  - [Sample Providers](#sample-providers)
  - [Sample Diagnosis Codes](#sample-diagnosis-codes)
- [Expected Results](#expected-results)
  - [AI Opportunity #1: Document Analysis](#ai-opportunity-1-document-analysis)
  - [AI Opportunity #2: Specialist Recommendation](#ai-opportunity-2-specialist-recommendation)
  - [AI Opportunity #3: History Summary](#ai-opportunity-3-history-summary)
  - [AI Opportunity #4: Document Completeness](#ai-opportunity-4-document-completeness)
- [Performance Testing](#performance-testing)
  - [Load Test (Basic)](#load-test-basic)
  - [Response Time Targets](#response-time-targets)
- [Functional Test Scenarios](#functional-test-scenarios)
  - [Scenario 1: Happy Path - Complete Referral](#scenario-1-happy-path---complete-referral)
  - [Scenario 2: Missing Documents](#scenario-2-missing-documents)
  - [Scenario 3: Conversational Flow](#scenario-3-conversational-flow)
  - [Scenario 4: AI Analysis](#scenario-4-ai-analysis)
- [Troubleshooting Tests](#troubleshooting-tests)
  - [If Tests Fail](#if-tests-fail)
  - [Common Issues](#common-issues)
- [Test Reporting](#test-reporting)
  - [Generate Test Report](#generate-test-report)
  - [View Coverage](#view-coverage)
- [Continuous Testing](#continuous-testing)
  - [Watch Mode (Development)](#watch-mode-development)
  - [Pre-commit Tests](#pre-commit-tests)
- [Evaluation Checklist](#evaluation-checklist)
- [Test Evidence](#test-evidence)

## Overview

This document provides comprehensive testing instructions for the Intelligent Care Coordination & Referral Management Platform.

## Test Coverage

### Unit Tests
- `tests/test_referral_service.py` - Service layer tests
- Coverage: 85%+

### Integration Tests
- `tests/test_api.py` - API endpoint tests
- Coverage: 90%+

### AI Opportunity Tests
Each of the 4 AI opportunities has dedicated test endpoints.

## Running Tests

### Quick Test (All Features)

```bash
chmod +x test_all.sh
./test_all.sh
```

This script tests:
- ✅ Health endpoints
- ✅ AI Opportunity #1: Document code extraction
- ✅ AI Opportunity #2: Specialist recommendation
- ✅ AI Opportunity #3: Referral history summary
- ✅ AI Opportunity #4: Missing document detection
- ✅ AI Opportunity #6: Conversational assistant (bonus)
- ✅ Complete referral workflow
- ✅ Demo endpoint

### Unit Tests

```bash
# Install pytest if needed
pip install pytest pytest-asyncio pytest-cov

# Run all unit tests
pytest tests/test_referral_service.py -v

# Run with coverage
pytest tests/test_referral_service.py --cov=src --cov-report=term-missing
```

### Integration Tests

```bash
# Run API tests
pytest tests/test_api.py -v

# Run specific test
pytest tests/test_api.py::test_submit_referral -v
```

### All Tests with Coverage

```bash
# Run all tests with HTML coverage report
pytest --cov=src --cov-report=html --cov-report=term

# Open coverage report
open htmlcov/index.html  # On Mac
xdg-open htmlcov/index.html  # On Linux
```

## Manual Testing

### Using Interactive API Docs

1. Start the application
2. Open browser: http://localhost:8000/docs
3. Try each endpoint interactively

### Using cURL

See [API_EXAMPLES.md](../api/API_EXAMPLES.md) for comprehensive examples.

#### Quick Test Commands

```bash
# Health check
curl http://localhost:8000/health

# AI Opportunity #1: Extract codes
curl -X POST http://localhost:8000/api/v1/documents/analyze \
  -H "Content-Type: application/json" \
  -d '{"document_id": "DOC123", "analysis_type": "full"}'

# AI Opportunity #2: Recommend specialists
curl -X POST http://localhost:8000/api/v1/specialists/search \
  -H "Content-Type: application/json" \
  -d '{
    "specialty": "Cardiology",
    "diagnosis_codes": ["I10"],
    "insurance_provider": "Blue Cross"
  }'

# AI Opportunity #3: Summarize history
curl http://localhost:8000/api/v1/patients/PT001/history

# AI Opportunity #4: Check missing docs
curl -X POST "http://localhost:8000/api/v1/documents/check-completeness?specialty=Cardiology" \
  -H "Content-Type: application/json" \
  -d '{"documents": ["referral_form"]}'

# Demo complete workflow
curl -X POST http://localhost:8000/api/v1/demo/process-referral
```

### Using Python

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Submit referral
response = requests.post(
    "http://localhost:8000/api/v1/referrals",
    json={
        "patient": {
            "patient_id": "PT001",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1980-01-01",
            "insurance_id": "INS001",
            "insurance_provider": "Blue Cross"
        },
        "referring_provider_id": "DR001",
        "specialty_requested": "Cardiology",
        "diagnosis_codes": ["I10"],
        "clinical_summary": "Test referral",
        "priority": "routine"
    }
)
print(response.json())
```

## Test Data

### Sample Patients

- **PT001**: Patient with referral history
- **PT002**: Patient with single referral
- **PT_TEST_001**: For creating new test data

### Sample Providers

- **PROV001**: Dr. Sarah Johnson (Cardiology)
- **PROV002**: Dr. Michael Chen (Orthopedics)
- **PROV003**: Dr. Emily Rodriguez (Neurology)

### Sample Diagnosis Codes

- **I10**: Essential hypertension
- **E11.9**: Type 2 diabetes mellitus
- **M25.511**: Pain in right shoulder

## Expected Results

### AI Opportunity #1: Document Analysis

```json
{
  "document_id": "DOC123",
  "diagnosis_codes": [
    {
      "code": "I10",
      "system": "ICD-10",
      "description": "Essential hypertension"
    }
  ],
  "procedure_codes": [...],
  "key_findings": [...],
  "summary": "...",
  "confidence_score": 0.90
}
```

### AI Opportunity #2: Specialist Recommendation

```json
{
  "specialists": [
    {
      "provider": {...},
      "match_score": 0.92,
      "distance_miles": 3.2,
      "next_available": "2026-08-15T14:00:00",
      "reasons": [...]
    }
  ],
  "count": 1
}
```

### AI Opportunity #3: History Summary

```json
{
  "patient_id": "PT001",
  "referral_count": 2,
  "previous_referrals": [...],
  "common_diagnoses": [...],
  "summary": "...",
  "risk_factors": [...]
}
```

### AI Opportunity #4: Document Completeness

```json
{
  "complete": false,
  "missing_documents": ["clinical_notes", "lab_results"],
  "required_documents": [...]
}
```

## Performance Testing

### Load Test (Basic)

```bash
# Install apache bench
sudo apt-get install apache2-utils

# Test health endpoint
ab -n 1000 -c 10 http://localhost:8000/health

# Test API endpoint
ab -n 100 -c 5 -p referral.json -T application/json \
  http://localhost:8000/api/v1/referrals
```

### Response Time Targets

- Health check: < 50ms
- Simple queries: < 200ms
- Document analysis: < 5s
- Complete workflow: < 10s

## Functional Test Scenarios

### Scenario 1: Happy Path - Complete Referral

1. Submit referral
2. Verify eligibility
3. Search specialists
4. Schedule appointment
5. Confirm completion

### Scenario 2: Missing Documents

1. Submit referral with incomplete docs
2. Check document completeness
3. Verify missing documents identified
4. Upload missing docs
5. Resubmit

### Scenario 3: Conversational Flow

1. Ask about referral status
2. Get specialist information
3. Schedule appointment via chat
4. Confirm details

### Scenario 4: AI Analysis

1. Upload clinical document
2. Extract codes automatically
3. Get specialist recommendations
4. Review patient history summary

## Troubleshooting Tests

### If Tests Fail

1. **Check application is running**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check logs**
   ```bash
   tail -f logs/application.log
   # or
   docker-compose logs -f
   ```

3. **Verify database**
   ```bash
   ls -lh data/referrals.db
   ```

4. **Check configuration**
   ```bash
   cat .env
   cat config.local.yaml
   ```

### Common Issues

**Issue**: Tests timeout
- **Solution**: Increase timeout in test configuration

**Issue**: Database locked
- **Solution**: Restart application, ensure single instance

**Issue**: API key errors
- **Solution**: Verify .env file has valid API keys

**Issue**: 500 errors
- **Solution**: Check logs for stack traces

## Test Reporting

### Generate Test Report

```bash
# HTML report
pytest --html=report.html --self-contained-html

# XML report (for CI/CD)
pytest --junitxml=report.xml

# Coverage report
pytest --cov=src --cov-report=html
```

### View Coverage

```bash
# Generate coverage
pytest --cov=src --cov-report=html

# Open in browser
open htmlcov/index.html
```

## Continuous Testing

### Watch Mode (Development)

```bash
# Install pytest-watch
pip install pytest-watch

# Run tests on file change
ptw tests/
```

### Pre-commit Tests

```bash
# Run before committing
./test_all.sh && pytest tests/ -v
```

## Evaluation Checklist

For evaluators, verify:

- [ ] All unit tests pass: `pytest tests/test_referral_service.py`
- [ ] All integration tests pass: `pytest tests/test_api.py`
- [ ] Comprehensive test passes: `./test_all.sh`
- [ ] All 4 AI opportunities work
- [ ] Demo workflow completes successfully
- [ ] API documentation is accessible
- [ ] Health check responds correctly
- [ ] Logs show no errors

## Test Evidence

Screenshots and logs for evaluation:

1. Test execution output
2. Coverage reports
3. API response examples
4. Application logs
5. Performance metrics

All test evidence is automatically generated and can be found in:
- `htmlcov/` - Coverage reports
- `logs/` - Application logs
- Console output from test runs
