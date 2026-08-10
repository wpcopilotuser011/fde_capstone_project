"""
Core Referral Service
Business logic for referral management
"""
from typing import List, Dict, Optional
from datetime import datetime
import uuid
from ..models import (
    ReferralRequest, ReferralResponse, ReferralStatus, ReferralPriority,
    EligibilityRequest, EligibilityResponse,
    SpecialistSearchRequest, SpecialistRecommendation,
    AppointmentRequest, AppointmentResponse,
    DocumentAnalysisRequest, DocumentAnalysisResponse,
    ReferralHistorySummary
)
from ..database import DatabaseManager, ReferralDB, PatientDB, ProviderDB, DocumentDB, AppointmentDB
from ..config import config
import logging

logger = logging.getLogger(__name__)


class ReferralService:
    """Core service for managing referrals"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.mock_mode = config.is_mock_mode()
    
    async def submit_referral(self, request: ReferralRequest) -> ReferralResponse:
        """Submit a new referral"""
        logger.info(f"Submitting referral for patient {request.patient.patient_id}")
        
        # Generate referral ID
        referral_id = f"REF{str(uuid.uuid4())[:8].upper()}"
        
        # Save patient if not exists
        session = self.db.get_session()
        try:
            patient = session.query(PatientDB).filter_by(
                patient_id=request.patient.patient_id
            ).first()
            
            if not patient:
                patient = PatientDB(
                    patient_id=request.patient.patient_id,
                    first_name=request.patient.first_name,
                    last_name=request.patient.last_name,
                    date_of_birth=request.patient.date_of_birth,
                    phone=request.patient.phone,
                    email=request.patient.email,
                    address=request.patient.address,
                    insurance_id=request.patient.insurance_id,
                    insurance_provider=request.patient.insurance_provider
                )
                session.add(patient)
            
            # Create referral
            referral = ReferralDB(
                referral_id=referral_id,
                patient_id=request.patient.patient_id,
                referring_provider_id=request.referring_provider_id,
                specialty_requested=request.specialty_requested,
                status=ReferralStatus.SUBMITTED.value,
                priority=request.priority.value,
                diagnosis_codes=request.diagnosis_codes,
                clinical_summary=request.clinical_summary,
                additional_data={
                    "preferred_location": request.preferred_location,
                    "additional_notes": request.additional_notes,
                    "documents": request.documents or []
                }
            )
            session.add(referral)
            session.commit()
            
            # Prepare response
            next_steps = [
                "Documents are being analyzed",
                "Insurance eligibility will be verified",
                "Specialist recommendations will be generated"
            ]
            
            response = ReferralResponse(
                referral_id=referral_id,
                status=ReferralStatus.SUBMITTED,
                patient_id=request.patient.patient_id,
                specialty_requested=request.specialty_requested,
                created_at=datetime.now(),
                estimated_wait_time=14,  # Default 2 weeks
                next_steps=next_steps
            )
            
            logger.info(f"Referral {referral_id} submitted successfully")
            return response
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error submitting referral: {e}")
            raise
        finally:
            session.close()
    
    async def get_referral_status(self, referral_id: str) -> Optional[ReferralResponse]:
        """Get referral status"""
        session = self.db.get_session()
        try:
            referral = session.query(ReferralDB).filter_by(referral_id=referral_id).first()
            
            if not referral:
                return None
            
            response = ReferralResponse(
                referral_id=referral.referral_id,
                status=ReferralStatus(referral.status),
                patient_id=referral.patient_id,
                specialty_requested=referral.specialty_requested,
                created_at=referral.created_at,
                estimated_wait_time=referral.estimated_wait_time,
                next_steps=self._get_next_steps(referral.status)
            )
            
            return response
            
        finally:
            session.close()
    
    def _get_next_steps(self, status: str) -> List[str]:
        """Get next steps based on status"""
        steps = {
            "submitted": ["Document analysis in progress", "Eligibility check pending"],
            "pending_eligibility": ["Insurance verification in progress"],
            "eligible": ["Searching for available specialists"],
            "specialist_assigned": ["Appointment scheduling in progress"],
            "appointment_scheduled": ["Appointment confirmed", "Check your email for details"],
            "completed": ["Referral completed successfully"],
            "cancelled": ["Referral has been cancelled"]
        }
        return steps.get(status, [])
    
    async def verify_eligibility(self, request: EligibilityRequest) -> EligibilityResponse:
        """Verify insurance eligibility (mock)"""
        logger.info(f"Verifying eligibility for patient {request.patient_id}")
        
        # Mock eligibility response
        response = EligibilityResponse(
            eligible=True,
            coverage_level="Gold",
            copay=40.0,
            deductible_remaining=500.0,
            prior_auth_required=False,
            messages=["Patient is eligible for specialist care", "In-network benefits apply"]
        )
        
        return response
    
    async def search_specialists(
        self,
        request: SpecialistSearchRequest
    ) -> List[SpecialistRecommendation]:
        """Search for specialists (calls MCP specialist_recommender)"""
        logger.info(f"Searching specialists for {request.specialty}")
        
        # This would call the MCP specialist_recommender server
        # For now, return mock data
        session = self.db.get_session()
        try:
            providers = session.query(ProviderDB).filter_by(
                specialty=request.specialty
            ).all()
            
            recommendations = []
            for provider in providers:
                # Check insurance match
                insurance_match = (
                    not request.insurance_provider or
                    request.insurance_provider in (provider.accepts_insurance or [])
                )
                
                if insurance_match:
                    from ..models import Provider
                    rec = SpecialistRecommendation(
                        provider=Provider(
                            provider_id=provider.provider_id,
                            first_name=provider.first_name,
                            last_name=provider.last_name,
                            specialty=provider.specialty,
                            npi=provider.npi,
                            phone=provider.phone,
                            email=provider.email,
                            address=provider.address,
                            accepts_insurance=provider.accepts_insurance
                        ),
                        match_score=0.85,
                        distance_miles=5.2,
                        next_available_slot=datetime(2026, 8, 15, 14, 0),
                        reason="Specialty match, in-network, highly rated"
                    )
                    recommendations.append(rec)
            
            return recommendations[:5]
            
        finally:
            session.close()
    
    async def schedule_appointment(
        self,
        request: AppointmentRequest
    ) -> AppointmentResponse:
        """Schedule appointment with specialist"""
        logger.info(f"Scheduling appointment for referral {request.referral_id}")
        
        appointment_id = f"APT{str(uuid.uuid4())[:8].upper()}"
        
        session = self.db.get_session()
        try:
            appointment = AppointmentDB(
                appointment_id=appointment_id,
                referral_id=request.referral_id,
                patient_id=request.patient_id,
                provider_id=request.provider_id,
                scheduled_time=datetime(2026, 8, 15, 14, 0),
                location="123 Medical Center Dr, Boston, MA",
                status="confirmed",
                confirmation_sent=1
            )
            session.add(appointment)
            
            # Update referral status
            referral = session.query(ReferralDB).filter_by(
                referral_id=request.referral_id
            ).first()
            if referral:
                referral.status = ReferralStatus.APPOINTMENT_SCHEDULED.value
                referral.appointment_id = appointment_id
            
            session.commit()
            
            response = AppointmentResponse(
                appointment_id=appointment_id,
                referral_id=request.referral_id,
                provider_id=request.provider_id,
                patient_id=request.patient_id,
                scheduled_time=appointment.scheduled_time,
                location=appointment.location,
                status="confirmed",
                confirmation_sent=True
            )
            
            return response
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error scheduling appointment: {e}")
            raise
        finally:
            session.close()


class DocumentService:
    """Service for document processing"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    async def analyze_document(
        self,
        request: DocumentAnalysisRequest
    ) -> DocumentAnalysisResponse:
        """Analyze document using AI (calls MCP document_processor)"""
        logger.info(f"Analyzing document {request.document_id}")
        
        # Mock response - in production, call MCP document_processor
        response = DocumentAnalysisResponse(
            document_id=request.document_id,
            diagnosis_codes=[
                {"code": "I10", "system": "ICD-10", "description": "Essential hypertension"}
            ],
            procedure_codes=[
                {"code": "99213", "system": "CPT", "description": "Office visit"}
            ],
            key_findings=[
                "Patient has history of hypertension",
                "Referred for cardiology evaluation"
            ],
            missing_information=[],
            summary="Patient referred for cardiology evaluation due to uncontrolled hypertension.",
            confidence_score=0.90
        )
        
        return response
    
    async def check_missing_documents(
        self,
        documents: List[str],
        specialty: str
    ) -> List[str]:
        """Check for missing required documents"""
        required_docs = {
            "Cardiology": ["referral_form", "clinical_notes", "lab_results", "insurance_card"],
            "Orthopedics": ["referral_form", "clinical_notes", "imaging_results", "insurance_card"],
            "Neurology": ["referral_form", "clinical_notes", "imaging_results", "insurance_card"]
        }
        
        required = required_docs.get(specialty, ["referral_form", "insurance_card"])
        missing = [doc for doc in required if doc not in documents]
        
        return missing


class HistoryService:
    """Service for referral history"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    async def get_patient_history(
        self,
        patient_id: str
    ) -> ReferralHistorySummary:
        """Get patient referral history summary"""
        session = self.db.get_session()
        try:
            referrals = session.query(ReferralDB).filter_by(
                patient_id=patient_id
            ).all()
            
            previous_refs = []
            diagnoses = []
            
            for ref in referrals:
                previous_refs.append({
                    "referral_id": ref.referral_id,
                    "specialty": ref.specialty_requested,
                    "date": ref.created_at.isoformat(),
                    "status": ref.status
                })
                diagnoses.extend(ref.diagnosis_codes or [])
            
            summary = f"Patient has {len(referrals)} previous referrals. " \
                     f"Common specialties: {', '.join(set([r.specialty_requested for r in referrals]))}"
            
            return ReferralHistorySummary(
                patient_id=patient_id,
                referral_count=len(referrals),
                previous_referrals=previous_refs,
                common_diagnoses=list(set(diagnoses)),
                summary=summary
            )
            
        finally:
            session.close()
