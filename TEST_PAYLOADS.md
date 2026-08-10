# 🧪 API TEST PAYLOADS
## Intelligent Referral Management Platform

**Server**: http://localhost:8000  
**Bedrock API**: Configured with Claude Sonnet 4.6  
**API Key**: sk-fvA7f_Ccz5nwx89qndDpRw  

---

## ✅ QUICK START - Test All Features

### 1️⃣ Health Check
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "ai_agents": "active",
  "bedrock_api": "configured"
}
```

---

## 🤖 AI OPPORTUNITY #1: Document Code Extraction

**Extract ICD-10 diagnosis codes and CPT procedure codes from clinical documents**

### Endpoint
```
POST /api/v1/documents/analyze
```

### Test Payload
```json
{
  "document_id": "DOC12345",
  "analysis_type": "full"
}
```

### cURL Command
```bash
curl -X POST http://localhost:8000/api/v1/documents/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "DOC12345",
    "analysis_type": "full"
  }'
```

### Expected Response
```json
{
  "document_id": "DOC12345",
  "diagnosis_codes": [
    {
      "code": "I10",
      "system": "ICD-10",
      "description": "Essential hypertension"
    },
    {
      "code": "E11.9",
      "system": "ICD-10",
      "description": "Type 2 diabetes mellitus"
    }
  ],
  "procedure_codes": [
    {
      "code": "99213",
      "system": "CPT",
      "description": "Office visit, established patient"
    }
  ],
  "key_findings": [
    "Patient has history of hypertension",
    "Recent diagnosis of type 2 diabetes",
    "Requires cardiology consultation"
  ],
  "summary": "Patient referred for cardiology evaluation...",
  "confidence_score": 0.90
}
```

---

## 🤖 AI OPPORTUNITY #2: Specialist Recommendation

**AI-powered specialist matching based on diagnosis, location, insurance, and availability**

### Endpoint
```
POST /api/v1/specialists/search
```

### Test Payload
```json
{
  "specialty": "Cardiology",
  "diagnosis_codes": ["I10", "E11.9"],
  "insurance_provider": "Blue Cross",
  "urgency": "routine"
}
```

### cURL Command
```bash
curl -X POST http://localhost:8000/api/v1/specialists/search \
  -H "Content-Type: application/json" \
  -d '{
    "specialty": "Cardiology",
    "diagnosis_codes": ["I10", "E11.9"],
    "insurance_provider": "Blue Cross",
    "urgency": "routine"
  }'
```

### Expected Response
```json
{
  "specialists": [
    {
      "provider": {
        "provider_id": "PROV001",
        "first_name": "Sarah",
        "last_name": "Johnson",
        "specialty": "Cardiology",
        "npi": "1234567890",
        "phone": "555-0101",
        "address": "123 Medical Center Dr, Boston, MA",
        "accepts_insurance": ["Blue Cross", "Aetna"]
      },
      "match_score": 0.92,
      "distance_miles": 3.2,
      "next_available_slot": "2026-08-15T14:00:00",
      "reasons": [
        "Specialty match: Cardiology",
        "In-network for Blue Cross",
        "High rating: 4.8/5.0"
      ],
      "wait_time_days": 5
    }
  ],
  "count": 1
}
```

---

## 🤖 AI OPPORTUNITY #3: Referral History Summary

**Generate AI-powered summary of patient's referral history for specialist review**

### Endpoint
```
GET /api/v1/patients/{patient_id}/history
```

### Test Request
```bash
curl http://localhost:8000/api/v1/patients/PT001/history
```

### Expected Response
```json
{
  "patient_id": "PT001",
  "referral_count": 2,
  "previous_referrals": [
    {
      "referral_id": "REF001",
      "specialty": "Cardiology",
      "date": "2025-12-10T00:00:00",
      "status": "completed"
    }
  ],
  "common_diagnoses": ["I10", "E11.9"],
  "summary": "Patient has 2 previous referrals. Common specialties: Cardiology, Endocrinology",
  "risk_factors": ["Cardiovascular risk factors present (HTN + DM)"]
}
```

---

## 🤖 AI OPPORTUNITY #4: Missing Document Detection

**Identify missing required documents before referral submission**

### Endpoint
```
POST /api/v1/documents/check-completeness?specialty=Cardiology
```

### Test Payload
```json
{
  "documents": ["referral_form", "insurance_card"]
}
```

### cURL Command
```bash
curl -X POST "http://localhost:8000/api/v1/documents/check-completeness?specialty=Cardiology" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": ["referral_form", "insurance_card"]
  }'
```

### Expected Response
```json
{
  "complete": false,
  "missing_documents": ["clinical_notes", "lab_results"],
  "required_documents": ["referral_form", "clinical_notes", "lab_results", "insurance_card"],
  "present_documents": ["referral_form", "insurance_card"],
  "completeness_score": 0.5
}
```

---

## 🎁 BONUS: AI OPPORTUNITY #6 - Conversational Assistant

**Answer patient queries through AI-powered natural language interface**

### Endpoint
```
POST /api/v1/conversation
```

### Test Payload
```json
{
  "user_id": "PT001",
  "message": "What is the status of my referral?"
}
```

### cURL Command
```bash
curl -X POST http://localhost:8000/api/v1/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "PT001",
    "message": "What is the status of my referral?"
  }'
```

### Expected Response
```json
{
  "session_id": "session_12345",
  "message": "I can help you check your referral status. Based on your recent referral, you've been referred to Dr. Sarah Johnson (Cardiology). Your appointment is scheduled for August 15, 2026 at 2:00 PM.",
  "intent": "check_status",
  "suggestions": [
    "Get directions to the appointment",
    "Reschedule appointment",
    "View required documents"
  ]
}
```

---

## 📋 COMPLETE REFERRAL SUBMISSION

**Submit a new referral (triggers all AI opportunities)**

### Endpoint
```
POST /api/v1/referrals
```

### Test Payload
```json
{
  "patient": {
    "patient_id": "PT001",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1980-05-15",
    "phone": "555-0100",
    "email": "john.doe@example.com",
    "insurance_id": "INS12345",
    "insurance_provider": "Blue Cross"
  },
  "referring_provider_id": "DR001",
  "specialty_requested": "Cardiology",
  "diagnosis_codes": ["I10", "E11.9"],
  "clinical_summary": "Patient with uncontrolled hypertension and type 2 diabetes. Requires cardiology evaluation.",
  "priority": "routine",
  "preferred_location": "Boston, MA"
}
```

### cURL Command
```bash
curl -X POST http://localhost:8000/api/v1/referrals \
  -H "Content-Type: application/json" \
  -d @referral_payload.json
```

### Expected Response
```json
{
  "referral_id": "REF00000001",
  "status": "submitted",
  "patient_id": "PT001",
  "specialty_requested": "Cardiology",
  "created_at": "2026-08-10T...",
  "estimated_wait_time": 14,
  "next_steps": [
    "Documents are being analyzed (AI #1)",
    "Checking document completeness (AI #4)",
    "Insurance eligibility will be verified",
    "Specialist recommendations will be generated (AI #2)"
  ]
}
```

---

## 🎯 COMPLETE WORKFLOW DEMO

**Demonstrates all 4 AI opportunities in one call**

### Endpoint
```
POST /api/v1/demo/process-referral
```

### Test Request
```bash
curl -X POST http://localhost:8000/api/v1/demo/process-referral
```

### Expected Response
```json
{
  "referral": {
    "referral_id": "REFDEMO123",
    "status": "submitted",
    "patient_id": "PT001",
    "specialty_requested": "Cardiology"
  },
  "ai_processing": {
    "completed_steps": [
      "document_analysis (AI #1)",
      "completeness_check (AI #4)",
      "eligibility_verification",
      "specialist_recommendation (AI #2)",
      "appointment_scheduling",
      "notifications_sent"
    ],
    "specialist": {
      "provider_id": "PROV001",
      "name": "Dr. Sarah Johnson",
      "specialty": "Cardiology",
      "rating": 4.8
    },
    "appointment": {
      "appointment_id": "APTDEMO123",
      "scheduled_time": "2026-08-15T14:00:00",
      "location": "123 Medical Center Dr",
      "status": "confirmed"
    }
  },
  "ai_capabilities_demonstrated": [
    "AI #1 - Document Code Extraction",
    "AI #2 - Specialist Recommendation",
    "AI #3 - Referral History Summary",
    "AI #4 - Missing Document Detection"
  ]
}
```

---

## 🔧 ADDITIONAL ENDPOINTS

### Get All Test Payloads
```bash
curl http://localhost:8000/payloads
```

### API Documentation
```bash
curl http://localhost:8000/docs
```

### Root Endpoint
```bash
curl http://localhost:8000/
```

---

## 📝 TESTING SCRIPT

**Run all tests in sequence:**

```bash
#!/bin/bash

echo "Testing AI Opportunity #1: Document Code Extraction"
curl -X POST http://localhost:8000/api/v1/documents/analyze \
  -H "Content-Type: application/json" \
  -d '{"document_id": "DOC123", "analysis_type": "full"}'
echo -e "\n\n"

echo "Testing AI Opportunity #2: Specialist Recommendation"
curl -X POST http://localhost:8000/api/v1/specialists/search \
  -H "Content-Type: application/json" \
  -d '{"specialty": "Cardiology", "diagnosis_codes": ["I10"], "insurance_provider": "Blue Cross"}'
echo -e "\n\n"

echo "Testing AI Opportunity #3: Referral History Summary"
curl http://localhost:8000/api/v1/patients/PT001/history
echo -e "\n\n"

echo "Testing AI Opportunity #4: Missing Document Detection"
curl -X POST "http://localhost:8000/api/v1/documents/check-completeness?specialty=Cardiology" \
  -H "Content-Type: application/json" \
  -d '{"documents": ["referral_form"]}'
echo -e "\n\n"

echo "Testing Complete Demo Workflow"
curl -X POST http://localhost:8000/api/v1/demo/process-referral
echo -e "\n\n"
```

---

## 🚀 FOR DEPLOYMENT ON TEKSTAC VM

1. **Copy project to VM**
2. **Ensure credentials are configured**:
   - `.env` file has: `OPENAI_API_KEY=sk-fvA7f_Ccz5nwx89qndDpRw`
   - `config.local.yaml` has Bedrock base URL

3. **Run with Docker**:
```bash
./build.sh
./run.sh
```

4. **Or run demo server**:
```bash
python3 demo_server.py
```

5. **Test with provided payloads above**

---

## ✅ EVALUATION CHECKLIST

- [ ] Health check responds: `curl http://localhost:8000/health`
- [ ] AI #1 works: Document code extraction
- [ ] AI #2 works: Specialist recommendation
- [ ] AI #3 works: Referral history summary
- [ ] AI #4 works: Missing document detection
- [ ] Complete workflow demo works
- [ ] All responses return proper JSON
- [ ] API documentation accessible

---

**All test payloads above can be used directly for evaluation!**
