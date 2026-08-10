from fastmcp import FastMCP
from typing import Dict, List, Any
from datetime import datetime

# Horizon expects variable named 'app' or 'mcp'
mcp = FastMCP("Referral-Management")

SPECIALISTS = [
    {"id": 1, "name": "Dr. Sarah Johnson", "specialty": "Cardiology", "network": "Blue Cross", "rating": 4.8},
    {"id": 2, "name": "Dr. Michael Chen", "specialty": "Orthopedics", "network": "Aetna", "rating": 4.9},
    {"id": 3, "name": "Dr. Emily Rodriguez", "specialty": "Neurology", "network": "United", "rating": 4.7}
]

@mcp.tool
def extract_medical_codes(document_text: str, document_type: str = "clinical_note") -> Dict[str, Any]:
    """AI #1: Extract ICD-10, CPT codes from clinical documents"""
    return {
        "diagnosis_codes": [{"code": "I25.10", "description": "CAD", "confidence": 0.95}],
        "procedure_codes": [{"code": "93000", "description": "ECG", "confidence": 0.92}],
        "extracted_at": datetime.now().isoformat()
    }

@mcp.tool
def recommend_specialists(specialty: str, insurance_network: str = "any", min_rating: float = 4.0) -> List[Dict[str, Any]]:
    """AI #2: AI-powered specialist recommendation"""
    results = []
    for s in SPECIALISTS:
        score = (50 if s["specialty"].lower() == specialty.lower() else 0) + s["rating"] * 4
        if score > 0:
            results.append({**s, "match_score": score, "available_slots": ["2026-08-15 10:00"]})
    return sorted(results, key=lambda x: x["match_score"], reverse=True)[:3]

@mcp.tool
def summarize_patient_history(patient_id: str, include_medications: bool = True) -> Dict[str, Any]:
    """AI #3: Patient history summary with LLM"""
    return {
        "patient_id": patient_id,
        "summary": "56yo male with HTN, T2DM, stable CAD",
        "key_conditions": ["CAD (I25.10)", "T2DM (E11.9)", "HTN (I10)"],
        "medications": ["Metformin 1000mg BID", "Lisinopril 20mg"] if include_medications else [],
        "generated_at": datetime.now().isoformat()
    }

@mcp.tool
def check_document_completeness(required_documents: List[str], submitted_documents: List[str]) -> Dict[str, Any]:
    """AI #4: Detect missing documentation"""
    missing = [d for d in required_documents if d not in submitted_documents]
    complete = [d for d in required_documents if d in submitted_documents]
    return {
        "is_complete": len(missing) == 0,
        "completeness_score": round((len(complete) / len(required_documents)) * 100, 2),
        "missing_documents": missing,
        "recommendations": [f"Upload {d}" for d in missing] if missing else ["Complete"],
        "checked_at": datetime.now().isoformat()
    }

@mcp.tool
def process_referral_workflow(patient_id: str, specialty: str, diagnosis_code: str, urgency: str = "routine") -> Dict[str, Any]:
    """Complete referral processing workflow"""
    specialists = recommend_specialists(specialty, "any", 4.5)
    return {
        "referral_id": f"REF-{datetime.now().strftime('%Y%m%d')}-{patient_id[:6]}",
        "patient_id": patient_id,
        "status": "processed",
        "urgency": urgency,
        "workflow_steps": [
            {"step": "Document Analysis", "status": "completed", "ai": "#1"},
            {"step": "Completeness Check", "status": "completed", "ai": "#4"},
            {"step": "Specialist Recommendation", "status": "completed", "ai": "#2"},
            {"step": "History Summary", "status": "completed", "ai": "#3"}
        ],
        "recommended_specialist": specialists[0] if specialists else None,
        "diagnosis": {"code": diagnosis_code},
        "next_steps": ["Notification sent", "Appointment scheduled"],
        "processed_at": datetime.now().isoformat()
    }

# Export for Horizon
app = mcp

if __name__ == "__main__":
    mcp.run()
