"""
Unit Tests for Referral Service
"""
import pytest
from datetime import datetime
from src.models import (
    ReferralRequest, Patient, ReferralPriority,
    EligibilityRequest, SpecialistSearchRequest
)
from src.database import DatabaseManager
from src.services.referral_service import ReferralService


@pytest.fixture
def db_manager():
    """Create test database"""
    db = DatabaseManager("data/test_referrals.db")
    db.init_sample_data()
    yield db
    # Cleanup
    import os
    if os.path.exists("data/test_referrals.db"):
        os.remove("data/test_referrals.db")


@pytest.fixture
def referral_service(db_manager):
    """Create referral service"""
    return ReferralService(db_manager)


@pytest.mark.asyncio
async def test_submit_referral(referral_service):
    """Test referral submission"""
    request = ReferralRequest(
        patient=Patient(
            patient_id="PT_TEST_001",
            first_name="Test",
            last_name="Patient",
            date_of_birth="1990-01-01",
            insurance_id="INS001",
            insurance_provider="Blue Cross"
        ),
        referring_provider_id="DR001",
        specialty_requested="Cardiology",
        diagnosis_codes=["I10"],
        clinical_summary="Test referral",
        priority=ReferralPriority.ROUTINE
    )
    
    response = await referral_service.submit_referral(request)
    
    assert response.referral_id is not None
    assert response.patient_id == "PT_TEST_001"
    assert response.specialty_requested == "Cardiology"
    assert response.status.value == "submitted"


@pytest.mark.asyncio
async def test_verify_eligibility(referral_service):
    """Test eligibility verification"""
    request = EligibilityRequest(
        patient_id="PT_TEST_001",
        insurance_id="INS001",
        insurance_provider="Blue Cross",
        service_type="specialist_visit"
    )
    
    response = await referral_service.verify_eligibility(request)
    
    assert response.eligible is True
    assert response.copay is not None


@pytest.mark.asyncio
async def test_search_specialists(referral_service):
    """Test specialist search"""
    request = SpecialistSearchRequest(
        specialty="Cardiology",
        diagnosis_codes=["I10"],
        insurance_provider="Blue Cross"
    )
    
    results = await referral_service.search_specialists(request)
    
    assert len(results) > 0
    assert results[0].provider.specialty == "Cardiology"


def test_get_next_steps(referral_service):
    """Test next steps generation"""
    steps = referral_service._get_next_steps("submitted")
    
    assert len(steps) > 0
    assert isinstance(steps, list)
