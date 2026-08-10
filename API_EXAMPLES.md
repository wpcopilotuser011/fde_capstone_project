# API Examples

## Example 1: Submit a Referral

```bash
curl -X POST http://localhost:8000/api/v1/referrals \
  -H "Content-Type: application/json" \
  -d '{
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
    "clinical_summary": "Patient with uncontrolled hypertension and diabetes. Requires cardiology evaluation.",
    "priority": "routine",
    "preferred_location": "Boston, MA"
  }'
```

**Response:**
```json
{
  "referral_id": "REFABC12345",
  "status": "submitted",
  "patient_id": "PT001",
  "specialty_requested": "Cardiology",
  "created_at": "2026-08-10T10:30:00",
  "estimated_wait_time": 14,
  "next_steps": [
    "Documents are being analyzed",
    "Insurance eligibility will be verified",
    "Specialist recommendations will be generated"
  ]
}
```

## Example 2: Check Eligibility

```bash
curl -X POST http://localhost:8000/api/v1/eligibility \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "PT001",
    "insurance_id": "INS12345",
    "insurance_provider": "Blue Cross",
    "service_type": "specialist_visit"
  }'
```

**Response:**
```json
{
  "eligible": true,
  "coverage_level": "Gold",
  "copay": 40.0,
  "deductible_remaining": 500.0,
  "prior_auth_required": false,
  "messages": [
    "Patient is eligible for specialist care",
    "In-network benefits apply"
  ]
}
```

## Example 3: AI-Powered Specialist Search

```bash
curl -X POST http://localhost:8000/api/v1/specialists/search \
  -H "Content-Type: application/json" \
  -d '{
    "specialty": "Cardiology",
    "diagnosis_codes": ["I10", "E11.9"],
    "insurance_provider": "Blue Cross",
    "patient_location": "Boston, MA",
    "urgency": "routine"
  }'
```

**Response:**
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
        "email": "sjohnson@hospital.com",
        "address": "123 Medical Center Dr, Boston, MA",
        "accepts_insurance": ["Blue Cross", "Aetna", "UnitedHealth"]
      },
      "match_score": 0.92,
      "distance_miles": 3.2,
      "next_available_slot": "2026-08-15T14:00:00",
      "reason": "Specialty match, in-network for Blue Cross, highly rated (4.8/5), available within 2 weeks"
    }
  ],
  "count": 1
}
```

## Example 4: Analyze Document (Extract Codes)

```bash
curl -X POST http://localhost:8000/api/v1/documents/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "DOC12345",
    "analysis_type": "full"
  }'
```

**Response:**
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
  "missing_information": [],
  "summary": "Patient referred for cardiology evaluation due to uncontrolled hypertension with new onset diabetes.",
  "confidence_score": 0.90
}
```

## Example 5: Check Document Completeness

```bash
curl -X POST "http://localhost:8000/api/v1/documents/check-completeness?specialty=Cardiology" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": ["referral_form", "insurance_card"]
  }'
```

**Response:**
```json
{
  "complete": false,
  "missing_documents": ["clinical_notes", "lab_results"],
  "required_documents": ["referral_form", "insurance_card"]
}
```

## Example 6: Conversational AI Assistant

```bash
curl -X POST http://localhost:8000/api/v1/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "PT001",
    "message": "What is the status of my referral?",
    "session_id": "session_123"
  }'
```

**Response:**
```json
{
  "session_id": "session_123",
  "message": "I can help you check your referral status. Based on your recent referral, you've been referred to Dr. Sarah Johnson (Cardiology). Your appointment is scheduled for August 15, 2026 at 2:00 PM. Your insurance eligibility has been verified and you're all set!",
  "suggestions": [
    "Get directions to the appointment",
    "Reschedule appointment",
    "View required documents"
  ],
  "actions_taken": ["status_checked"]
}
```

## Example 7: Get Patient History Summary

```bash
curl -X GET http://localhost:8000/api/v1/patients/PT001/history
```

**Response:**
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
    },
    {
      "referral_id": "REF002",
      "specialty": "Endocrinology",
      "date": "2026-03-15T00:00:00",
      "status": "completed"
    }
  ],
  "common_diagnoses": ["I10", "E11.9"],
  "summary": "Patient has 2 previous referrals. Common specialties: Cardiology, Endocrinology",
  "risk_factors": ["Cardiovascular risk factors present (HTN + DM)"]
}
```

## Example 8: Schedule Appointment

```bash
curl -X POST http://localhost:8000/api/v1/appointments \
  -H "Content-Type: application/json" \
  -d '{
    "referral_id": "REFABC12345",
    "provider_id": "PROV001",
    "patient_id": "PT001",
    "preferred_dates": ["2026-08-15", "2026-08-16"],
    "preferred_time": "afternoon"
  }'
```

**Response:**
```json
{
  "appointment_id": "APTABC12345",
  "referral_id": "REFABC12345",
  "provider_id": "PROV001",
  "patient_id": "PT001",
  "scheduled_time": "2026-08-15T14:00:00",
  "location": "123 Medical Center Dr, Boston, MA",
  "status": "confirmed",
  "confirmation_sent": true
}
```

## Example 9: Upload Document

```bash
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@referral_form.pdf" \
  -F "document_type=referral_form"
```

**Response:**
```json
{
  "document_id": "DOCXYZ789",
  "filename": "referral_form.pdf",
  "document_type": "referral_form",
  "file_path": "data/uploads/referral_form.pdf",
  "size": 45678,
  "uploaded_at": "2026-08-10T11:00:00"
}
```

## Example 10: Complete Workflow Demo

```bash
curl -X POST http://localhost:8000/api/v1/demo/process-referral
```

**Response:**
```json
{
  "referral": {
    "referral_id": "REFDEMO123",
    "status": "submitted",
    "patient_id": "PT001",
    "specialty_requested": "Cardiology",
    "created_at": "2026-08-10T11:15:00",
    "estimated_wait_time": 14,
    "next_steps": [
      "Documents are being analyzed",
      "Insurance eligibility will be verified",
      "Specialist recommendations will be generated"
    ]
  },
  "ai_processing": {
    "completed_steps": [
      "document_analysis",
      "completeness_check",
      "eligibility_verification",
      "specialist_recommendation",
      "appointment_scheduling",
      "notifications_sent"
    ],
    "current_step": "completed",
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
  }
}
```

## Using Python Requests

```python
import requests

# Submit referral
response = requests.post(
    "http://localhost:8000/api/v1/referrals",
    json={
        "patient": {
            "patient_id": "PT001",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1980-05-15",
            "insurance_id": "INS12345",
            "insurance_provider": "Blue Cross"
        },
        "referring_provider_id": "DR001",
        "specialty_requested": "Cardiology",
        "diagnosis_codes": ["I10"],
        "clinical_summary": "Patient with hypertension",
        "priority": "routine"
    }
)

print(response.json())
```
