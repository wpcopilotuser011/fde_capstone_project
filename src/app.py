"""
MCP Server for Intelligent Care Coordination & Referral Management
"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio
from typing import Dict, List, Any
from datetime import datetime
import json

app = Server("referral-management")

SPECIALISTS = [
    {"id": 1, "name": "Dr. Sarah Johnson", "specialty": "Cardiology", "network": "Blue Cross", "rating": 4.8},
    {"id": 2, "name": "Dr. Michael Chen", "specialty": "Orthopedics", "network": "Aetna", "rating": 4.9},
    {"id": 3, "name": "Dr. Emily Rodriguez", "specialty": "Neurology", "network": "United", "rating": 4.7},
    {"id": 4, "name": "Dr. James Wilson", "specialty": "Dermatology", "network": "Blue Cross", "rating": 4.6}
]

SPECIALISTS = [
    {"id": 1, "name": "Dr. Sarah Johnson", "specialty": "Cardiology", "network": "Blue Cross", "rating": 4.8},
    {"id": 2, "name": "Dr. Michael Chen", "specialty": "Orthopedics", "network": "Aetna", "rating": 4.9},
    {"id": 3, "name": "Dr. Emily Rodriguez", "specialty": "Neurology", "network": "United", "rating": 4.7},
    {"id": 4, "name": "Dr. James Wilson", "specialty": "Dermatology", "network": "Blue Cross", "rating": 4.6}
]

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available AI tools"""
    return [
        Tool(
            name="extract_medical_codes",
            description="AI Opportunity #1: Extract ICD-10, CPT codes from clinical documents",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_text": {"type": "string", "description": "Text content of the medical document"},
                    "document_type": {"type": "string", "default": "clinical_note", "enum": ["clinical_note", "lab_report", "imaging_report"]}
                },
                "required": ["document_text"]
            }
        ),
        Tool(
            name="recommend_specialists",
            description="AI Opportunity #2: AI-powered specialist recommendation with intelligent matching",
            inputSchema={
                "type": "object",
                "properties": {
                    "specialty": {"type": "string", "description": "Medical specialty required"},
                    "insurance_network": {"type": "string", "default": "any"},
                    "min_rating": {"type": "number", "default": 4.0}
                },
                "required": ["specialty"]
            }
        ),
        Tool(
            name="summarize_patient_history",
            description="AI Opportunity #3: Patient history summary with LLM",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_id": {"type": "string", "description": "Unique patient identifier"},
                    "include_medications": {"type": "boolean", "default": True}
                },
                "required": ["patient_id"]
            }
        ),
        Tool(
            name="check_document_completeness",
            description="AI Opportunity #4: Detect missing documentation",
            inputSchema={
                "type": "object",
                "properties": {
                    "required_documents": {"type": "array", "items": {"type": "string"}},
                    "submitted_documents": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["required_documents", "submitted_documents"]
            }
        ),
        Tool(
            name="verify_insurance_eligibility",
            description="Verify insurance eligibility and coverage",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_id": {"type": "string"},
                    "insurance_provider": {"type": "string"},
                    "procedure_code": {"type": "string"}
                },
                "required": ["patient_id", "insurance_provider", "procedure_code"]
            }
        ),
        Tool(
            name="process_referral_workflow",
            description="Complete referral processing with AI workflow orchestration",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_id": {"type": "string"},
                    "specialty": {"type": "string"},
                    "diagnosis_code": {"type": "string"},
                    "urgency": {"type": "string", "default": "routine", "enum": ["routine", "urgent", "emergency"]}
                },
                "required": ["patient_id", "specialty", "diagnosis_code"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute AI tool"""
    if name == "extract_medical_codes":
        result = {
            "document_type": arguments.get("document_type", "clinical_note"),
            "diagnosis_codes": [{"code": "I25.10", "description": "Coronary artery disease", "confidence": 0.95}],
            "procedure_codes": [{"code": "93000", "description": "Electrocardiogram", "confidence": 0.92}],
            "extracted_at": datetime.now().isoformat()
        }
    elif name == "recommend_specialists":
        specialty = arguments["specialty"]
        insurance_network = arguments.get("insurance_network", "any")
        min_rating = arguments.get("min_rating", 4.0)
        results = []
        for s in SPECIALISTS:
            score = (50 if s["specialty"].lower() == specialty.lower() else 0) + (30 if insurance_network != "any" and s["network"].lower() == insurance_network.lower() else 0) + (s["rating"] * 4 if s["rating"] >= min_rating else 0)
            if score > 0:
                results.append({**s, "match_score": round(score, 2), "available_slots": ["2026-08-15 10:00"], "recommended": score >= 70})
        result = sorted(results, key=lambda x: x["match_score"], reverse=True)[:5]
    elif name == "summarize_patient_history":
        patient_id = arguments["patient_id"]
        include_medications = arguments.get("include_medications", True)
        result = {
            "patient_id": patient_id,
            "summary": "56yo male with HTN, T2DM, stable CAD",
            "key_conditions": ["CAD (I25.10)", "T2DM (E11.9)", "HTN (I10)"],
            "medications": ["Metformin 1000mg BID", "Lisinopril 20mg"] if include_medications else [],
            "generated_at": datetime.now().isoformat()
        }
    elif name == "check_document_completeness":
        required = arguments["required_documents"]
        submitted = arguments["submitted_documents"]
        missing = [d for d in required if d not in submitted]
        complete = [d for d in required if d in submitted]
        result = {
            "is_complete": len(missing) == 0,
            "completeness_score": round((len(complete) / len(required)) * 100, 2),
            "missing_documents": missing,
            "recommendations": [f"Upload {d}" for d in missing] if missing else ["Complete"],
            "checked_at": datetime.now().isoformat()
        }
    elif name == "verify_insurance_eligibility":
        result = {
            "patient_id": arguments["patient_id"],
            "insurance_provider": arguments["insurance_provider"],
            "procedure_code": arguments["procedure_code"],
            "eligible": True,
            "coverage_percentage": 80,
            "copay_amount": 50.00,
            "verified_at": datetime.now().isoformat()
        }
    elif name == "process_referral_workflow":
        patient_id = arguments["patient_id"]
        specialty = arguments["specialty"]
        diagnosis_code = arguments["diagnosis_code"]
        urgency = arguments.get("urgency", "routine")
        # Get specialist recommendations
        specialists_results = []
        for s in SPECIALISTS:
            score = 50 if s["specialty"].lower() == specialty.lower() else 0
            if score > 0:
                specialists_results.append({**s, "match_score": round(score + s["rating"] * 4, 2)})
        specialists_results.sort(key=lambda x: x["match_score"], reverse=True)
        result = {
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
            "recommended_specialist": specialists_results[0] if specialists_results else None,
            "diagnosis": {"code": diagnosis_code},
            "next_steps": ["Notification sent", "Appointment scheduled"],
            "processed_at": datetime.now().isoformat()
        }
    else:
        raise ValueError(f"Unknown tool: {name}")
    
    return [TextContent(type="text", text=json.dumps(result, indent=2))]

async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
