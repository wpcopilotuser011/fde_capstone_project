"""
Data Models for the Referral Management System
"""
from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field


class ReferralStatus(str, Enum):
    """Referral status enumeration"""
    SUBMITTED = "submitted"
    PENDING_ELIGIBILITY = "pending_eligibility"
    ELIGIBLE = "eligible"
    INELIGIBLE = "ineligible"
    SPECIALIST_ASSIGNED = "specialist_assigned"
    APPOINTMENT_SCHEDULED = "appointment_scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ReferralPriority(str, Enum):
    """Referral priority enumeration"""
    ROUTINE = "routine"
    URGENT = "urgent"
    EMERGENT = "emergent"


class DocumentType(str, Enum):
    """Document type enumeration"""
    REFERRAL_FORM = "referral_form"
    CLINICAL_NOTES = "clinical_notes"
    LAB_RESULTS = "lab_results"
    IMAGING_RESULTS = "imaging_results"
    INSURANCE_CARD = "insurance_card"
    PRIOR_AUTH = "prior_authorization"


# Request/Response Models

class Patient(BaseModel):
    """Patient information"""
    patient_id: str
    first_name: str
    last_name: str
    date_of_birth: str
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    insurance_id: Optional[str] = None
    insurance_provider: Optional[str] = None


class Provider(BaseModel):
    """Healthcare provider information"""
    provider_id: str
    first_name: str
    last_name: str
    specialty: str
    npi: str  # National Provider Identifier
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    accepts_insurance: Optional[List[str]] = None


class DiagnosisCode(BaseModel):
    """Diagnosis code information"""
    code: str
    system: str = "ICD-10"  # ICD-10, ICD-9, etc.
    description: str


class ProcedureCode(BaseModel):
    """Procedure code information"""
    code: str
    system: str = "CPT"  # CPT, HCPCS, etc.
    description: str


class ClinicalDocument(BaseModel):
    """Clinical document metadata"""
    document_id: str
    document_type: DocumentType
    file_path: str
    uploaded_at: datetime = Field(default_factory=datetime.now)
    extracted_data: Optional[dict] = None


class ReferralRequest(BaseModel):
    """Referral submission request"""
    patient: Patient
    referring_provider_id: str
    specialty_requested: str
    diagnosis_codes: List[str]
    clinical_summary: str
    priority: ReferralPriority = ReferralPriority.ROUTINE
    documents: Optional[List[str]] = None  # List of document IDs
    preferred_location: Optional[str] = None
    additional_notes: Optional[str] = None


class ReferralResponse(BaseModel):
    """Referral submission response"""
    referral_id: str
    status: ReferralStatus
    patient_id: str
    specialty_requested: str
    created_at: datetime
    estimated_wait_time: Optional[int] = None  # in days
    next_steps: List[str] = []
    missing_documents: Optional[List[str]] = None


class EligibilityRequest(BaseModel):
    """Insurance eligibility check request"""
    patient_id: str
    insurance_id: str
    insurance_provider: str
    service_type: str
    provider_npi: Optional[str] = None


class EligibilityResponse(BaseModel):
    """Insurance eligibility check response"""
    eligible: bool
    coverage_level: Optional[str] = None
    copay: Optional[float] = None
    deductible_remaining: Optional[float] = None
    prior_auth_required: bool = False
    messages: List[str] = []


class SpecialistRecommendation(BaseModel):
    """Specialist recommendation"""
    provider: Provider
    match_score: float  # 0-1 score
    distance_miles: Optional[float] = None
    next_available_slot: Optional[datetime] = None
    reason: str  # Why this specialist was recommended


class SpecialistSearchRequest(BaseModel):
    """Specialist search request"""
    specialty: str
    diagnosis_codes: List[str]
    patient_location: Optional[str] = None
    insurance_provider: Optional[str] = None
    max_distance_miles: Optional[float] = 50.0
    urgency: ReferralPriority = ReferralPriority.ROUTINE


class AppointmentRequest(BaseModel):
    """Appointment scheduling request"""
    referral_id: str
    provider_id: str
    patient_id: str
    preferred_dates: Optional[List[str]] = None
    preferred_time: Optional[str] = None  # morning, afternoon, evening


class AppointmentResponse(BaseModel):
    """Appointment scheduling response"""
    appointment_id: str
    referral_id: str
    provider_id: str
    patient_id: str
    scheduled_time: datetime
    location: str
    status: str
    confirmation_sent: bool = False


class ConversationRequest(BaseModel):
    """Conversation/chat request"""
    session_id: Optional[str] = None
    user_id: str
    message: str
    context: Optional[dict] = None


class ConversationResponse(BaseModel):
    """Conversation/chat response"""
    session_id: str
    message: str
    suggestions: Optional[List[str]] = None
    actions_taken: Optional[List[str]] = None


class DocumentAnalysisRequest(BaseModel):
    """Document analysis request"""
    document_id: str
    analysis_type: str = "full"  # full, extract_codes, check_completeness


class DocumentAnalysisResponse(BaseModel):
    """Document analysis response"""
    document_id: str
    diagnosis_codes: List[DiagnosisCode] = []
    procedure_codes: List[ProcedureCode] = []
    key_findings: List[str] = []
    missing_information: List[str] = []
    summary: Optional[str] = None
    confidence_score: float = 0.0


class ReferralHistorySummary(BaseModel):
    """Referral history summary for specialist"""
    patient_id: str
    referral_count: int
    previous_referrals: List[dict]
    common_diagnoses: List[str]
    summary: str
    risk_factors: Optional[List[str]] = None
