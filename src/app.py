from fastmcp import FastMCP
from typing import Dict, List, Any
from datetime import datetime

mcp = FastMCP("Referral Management")

SPECIALISTS = [
    {"id": 1, "name": "Dr. Sarah Johnson", "specialty": "Cardiology", "network": "Blue Cross", "rating": 4.8},
    {"id": 2, "name": "Dr. Michael Chen", "specialty": "Orthopedics", "network": "Aetna", "rating": 4.9},
    {"id": 3, "name": "Dr. Emily Rodriguez", "specialty": "Neurology", "network": "United", "rating": 4.7}
]

@mcp.tool()
def extract_medical_codes(document_text: str, document_type: str = "clinical_note") -> Dict[str, Any]:
    """AI #1: Extract ICD-10, CPT codes"""
    return {"diagnosis_codes": [{"code": "I25.10", "description": "CAD", "confidence": 0.95}], "procedure_codes": [{"code": "93000", "description": "ECG", "confidence": 0.92}]}

@mcp.tool()
def recommend_specialists(specialty: str, insurance_network: str = "any", min_rating: float = 4.0) -> List[Dict[str, Any]]:
    """AI #2: Specialist recommendation"""
    results = []
    for s in SPECIALISTS:
        score = (50 if s["specialty"].lower() == specialty.lower() else 0) + (30 if insurance_network != "any" and s["network"].lower() == insurance_network.lower() else 0) + s["rating"] * 4
        if score > 0:
            results.append({**s, "match_score": score})
    return sorted(results, key=lambda x: x["match_score"], reverse=True)[:3]

@mcp.tool()
def summarize_patient_history(patient_id: str, include_medications: bool = True) -> Dict[str, Any]:
    """AI #3: Patient history summary"""
    return {"patient_id": patient_id, "summary": "56yo male HTN/T2DM/CAD", "conditions": ["CAD", "T2DM", "HTN"], "medications": ["Metformin", "Lisinopril"] if include_medications else []}

@mcp.tool()
def check_document_completeness(required_documents: List[str], submitted_documents: List[str]) -> Dict[str, Any]:
    """AI #4: Missing document detection"""
    missing = [d for d in required_documents if d not in submitted_documents]
    return {"is_complete": not missing, "completeness_score": round((len(required_documents) - len(missing)) / len(required_documents) * 100), "missing": missing}

@mcp.tool()
def verify_insurance(patient_id: str, insurance_provider: str, procedure_code: str) -> Dict[str, Any]:
    """Verify insurance eligibility"""
    return {"patient_id": patient_id, "eligible": True, "coverage": 80, "copay": 50.00}

@mcp.tool()
def process_referral(patient_id: str, specialty: str, diagnosis_code: str, urgency: str = "routine") -> Dict[str, Any]:
    """Complete referral workflow"""
    specialists = recommend_specialists(specialty, "any", 4.5)
    return {"referral_id": f"REF-{datetime.now().strftime('%Y%m%d')}-{patient_id[:6]}", "status": "processed", "urgency": urgency, "workflow": [{"step": "Analysis", "ai": "#1"}, {"step": "Completeness", "ai": "#4"}, {"step": "Recommendation", "ai": "#2"}], "specialist": specialists[0] if specialists else None}

app = mcp
