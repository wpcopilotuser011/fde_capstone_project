"""
Integration Tests for API Endpoints
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_submit_referral(client):
    """Test referral submission"""
    referral_data = {
        "patient": {
            "patient_id": "PT_API_TEST_001",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1980-01-01",
            "insurance_id": "INS001",
            "insurance_provider": "Blue Cross"
        },
        "referring_provider_id": "DR001",
        "specialty_requested": "Cardiology",
        "diagnosis_codes": ["I10"],
        "clinical_summary": "Test referral via API",
        "priority": "routine"
    }
    
    response = client.post("/api/v1/referrals", json=referral_data)
    assert response.status_code == 200
    data = response.json()
    assert "referral_id" in data
    assert data["specialty_requested"] == "Cardiology"


def test_check_eligibility(client):
    """Test eligibility check"""
    eligibility_data = {
        "patient_id": "PT001",
        "insurance_id": "INS001",
        "insurance_provider": "Blue Cross",
        "service_type": "specialist_visit"
    }
    
    response = client.post("/api/v1/eligibility", json=eligibility_data)
    assert response.status_code == 200
    data = response.json()
    assert "eligible" in data


def test_search_specialists(client):
    """Test specialist search"""
    search_data = {
        "specialty": "Cardiology",
        "diagnosis_codes": ["I10"]
    }
    
    response = client.post("/api/v1/specialists/search", json=search_data)
    assert response.status_code == 200
    data = response.json()
    assert "specialists" in data


def test_conversation(client):
    """Test conversational AI"""
    conversation_data = {
        "user_id": "PT001",
        "message": "What is the status of my referral?"
    }
    
    response = client.post("/api/v1/conversation", json=conversation_data)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "session_id" in data


def test_document_upload(client):
    """Test document upload"""
    files = {'file': ('test.txt', b'Test document content', 'text/plain')}
    data = {'document_type': 'referral_form'}
    
    response = client.post("/api/v1/documents/upload", files=files, data=data)
    assert response.status_code == 200
    result = response.json()
    assert "document_id" in result


def test_demo_endpoint(client):
    """Test demo workflow"""
    response = client.post("/api/v1/demo/process-referral")
    assert response.status_code == 200
    data = response.json()
    assert "referral" in data
