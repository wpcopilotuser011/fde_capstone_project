#!/usr/bin/env python3
"""
Standalone API Demo Server - No External Dependencies Required
Demonstrates all 4 AI Opportunities with mock responses
"""

import json
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# Sample data storage
referrals = {}
referral_counter = 1

class APIHandler(BaseHTTPRequestHandler):
    
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers()
    
    def do_GET(self):
        if self.path == '/':
            self._set_headers()
            response = {
                "status": "healthy",
                "service": "Intelligent Referral Management Platform",
                "version": "1.0.0",
                "timestamp": datetime.datetime.now().isoformat(),
                "api_docs": "See /docs for all endpoints"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        
        elif self.path == '/health':
            self._set_headers()
            response = {
                "status": "healthy",
                "database": "connected",
                "ai_agents": "active",
                "bedrock_api": "configured"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        
        elif self.path == '/docs':
            self._set_headers()
            response = {
                "message": "API Documentation",
                "endpoints": [
                    {
                        "method": "POST",
                        "path": "/api/v1/referrals",
                        "description": "Submit new referral",
                        "ai_opportunity": "All 4"
                    },
                    {
                        "method": "POST",
                        "path": "/api/v1/documents/analyze",
                        "description": "AI #1: Extract diagnosis and procedure codes",
                        "ai_opportunity": "#1"
                    },
                    {
                        "method": "POST",
                        "path": "/api/v1/specialists/search",
                        "description": "AI #2: Recommend specialists",
                        "ai_opportunity": "#2"
                    },
                    {
                        "method": "GET",
                        "path": "/api/v1/patients/{patient_id}/history",
                        "description": "AI #3: Summarize referral history",
                        "ai_opportunity": "#3"
                    },
                    {
                        "method": "POST",
                        "path": "/api/v1/documents/check-completeness",
                        "description": "AI #4: Identify missing documents",
                        "ai_opportunity": "#4"
                    },
                    {
                        "method": "POST",
                        "path": "/api/v1/conversation",
                        "description": "AI #6: Conversational assistant",
                        "ai_opportunity": "#6 (Bonus)"
                    },
                    {
                        "method": "POST",
                        "path": "/api/v1/demo/process-referral",
                        "description": "Complete workflow demo"
                    }
                ],
                "test_payloads": "/payloads"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        
        elif self.path == '/payloads':
            self._set_headers()
            self.wfile.write(self._get_test_payloads().encode())
        
        elif self.path.startswith('/api/v1/patients/'):
            # AI Opportunity #3: Patient History Summary
            self._set_headers()
            response = {
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
                "risk_factors": ["Cardiovascular risk factors present (HTN + DM)"],
                "ai_capability": "AI Opportunity #3 - Referral History Summary"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
        
        try:
            data = json.loads(post_data) if post_data else {}
        except:
            data = {}
        
        if self.path == '/api/v1/documents/analyze':
            # AI Opportunity #1: Document Code Extraction
            self._set_headers()
            response = {
                "document_id": data.get("document_id", "DOC123"),
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
                "confidence_score": 0.90,
                "ai_capability": "AI Opportunity #1 - Document Code Extraction"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        
        elif self.path == '/api/v1/specialists/search':
            # AI Opportunity #2: Specialist Recommendation
            self._set_headers()
            response = {
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
                        "reasons": [
                            "Specialty match: Cardiology",
                            "In-network for Blue Cross",
                            "High rating: 4.8/5.0",
                            "Available within 2 weeks"
                        ],
                        "wait_time_days": 5
                    }
                ],
                "count": 1,
                "ai_capability": "AI Opportunity #2 - Specialist Recommendation"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        
        elif self.path.startswith('/api/v1/documents/check-completeness'):
            # AI Opportunity #4: Missing Document Detection
            self._set_headers()
            response = {
                "complete": False,
                "missing_documents": ["clinical_notes", "lab_results"],
                "required_documents": ["referral_form", "clinical_notes", "lab_results", "insurance_card"],
                "present_documents": data.get("documents", ["referral_form", "insurance_card"]),
                "completeness_score": 0.5,
                "ai_capability": "AI Opportunity #4 - Missing Document Detection"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        
        elif self.path == '/api/v1/conversation':
            # AI Opportunity #6: Conversational Assistant
            self._set_headers()
            response = {
                "session_id": data.get("session_id", f"session_{datetime.datetime.now().timestamp()}"),
                "message": "I can help you check your referral status. Based on your recent referral, you've been referred to Dr. Sarah Johnson (Cardiology). Your appointment is scheduled for August 15, 2026 at 2:00 PM. Your insurance eligibility has been verified and you're all set!",
                "intent": "check_status",
                "suggestions": [
                    "Get directions to the appointment",
                    "Reschedule appointment",
                    "View required documents"
                ],
                "actions_taken": ["status_checked"],
                "ai_capability": "AI Opportunity #6 - Conversational Assistant"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        
        elif self.path == '/api/v1/referrals':
            # Submit Referral
            global referral_counter
            self._set_headers()
            referral_id = f"REF{str(referral_counter).zfill(8)}"
            referral_counter += 1
            
            response = {
                "referral_id": referral_id,
                "status": "submitted",
                "patient_id": data.get("patient", {}).get("patient_id", "PT001"),
                "specialty_requested": data.get("specialty_requested", "Cardiology"),
                "created_at": datetime.datetime.now().isoformat(),
                "estimated_wait_time": 14,
                "next_steps": [
                    "Documents are being analyzed (AI #1)",
                    "Checking document completeness (AI #4)",
                    "Insurance eligibility will be verified",
                    "Specialist recommendations will be generated (AI #2)"
                ]
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        
        elif self.path == '/api/v1/demo/process-referral':
            # Complete Demo Workflow
            self._set_headers()
            response = {
                "referral": {
                    "referral_id": "REFDEMO123",
                    "status": "submitted",
                    "patient_id": "PT001",
                    "specialty_requested": "Cardiology",
                    "created_at": datetime.datetime.now().isoformat()
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
            self.wfile.write(json.dumps(response, indent=2).encode())
        
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())
    
    def _get_test_payloads(self):
        payloads = {
            "message": "Test Payloads for All AI Opportunities",
            "payloads": {
                "1_document_analysis": {
                    "endpoint": "POST /api/v1/documents/analyze",
                    "description": "AI Opportunity #1: Extract diagnosis and procedure codes",
                    "payload": {
                        "document_id": "DOC12345",
                        "analysis_type": "full"
                    },
                    "curl": 'curl -X POST http://localhost:8000/api/v1/documents/analyze -H "Content-Type: application/json" -d \'{"document_id": "DOC12345", "analysis_type": "full"}\''
                },
                "2_specialist_search": {
                    "endpoint": "POST /api/v1/specialists/search",
                    "description": "AI Opportunity #2: Recommend specialists",
                    "payload": {
                        "specialty": "Cardiology",
                        "diagnosis_codes": ["I10", "E11.9"],
                        "insurance_provider": "Blue Cross",
                        "urgency": "routine"
                    },
                    "curl": 'curl -X POST http://localhost:8000/api/v1/specialists/search -H "Content-Type: application/json" -d \'{"specialty": "Cardiology", "diagnosis_codes": ["I10"], "insurance_provider": "Blue Cross"}\''
                },
                "3_patient_history": {
                    "endpoint": "GET /api/v1/patients/PT001/history",
                    "description": "AI Opportunity #3: Summarize referral history",
                    "payload": "No payload needed (GET request)",
                    "curl": "curl http://localhost:8000/api/v1/patients/PT001/history"
                },
                "4_document_completeness": {
                    "endpoint": "POST /api/v1/documents/check-completeness?specialty=Cardiology",
                    "description": "AI Opportunity #4: Identify missing documents",
                    "payload": {
                        "documents": ["referral_form", "insurance_card"]
                    },
                    "curl": 'curl -X POST "http://localhost:8000/api/v1/documents/check-completeness?specialty=Cardiology" -H "Content-Type: application/json" -d \'{"documents": ["referral_form", "insurance_card"]}\''
                },
                "5_conversation": {
                    "endpoint": "POST /api/v1/conversation",
                    "description": "AI Opportunity #6: Conversational assistant (Bonus)",
                    "payload": {
                        "user_id": "PT001",
                        "message": "What is the status of my referral?"
                    },
                    "curl": 'curl -X POST http://localhost:8000/api/v1/conversation -H "Content-Type: application/json" -d \'{"user_id": "PT001", "message": "What is the status of my referral?"}\''
                },
                "6_submit_referral": {
                    "endpoint": "POST /api/v1/referrals",
                    "description": "Submit new referral (demonstrates all AI opportunities)",
                    "payload": {
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
                        "diagnosis_codes": ["I10", "E11.9"],
                        "clinical_summary": "Patient with uncontrolled hypertension and diabetes",
                        "priority": "routine"
                    },
                    "curl": 'curl -X POST http://localhost:8000/api/v1/referrals -H "Content-Type: application/json" -d @referral_payload.json'
                },
                "7_demo_workflow": {
                    "endpoint": "POST /api/v1/demo/process-referral",
                    "description": "Complete workflow demonstrating all 4 AI opportunities",
                    "payload": "No payload needed",
                    "curl": "curl -X POST http://localhost:8000/api/v1/demo/process-referral"
                }
            }
        }
        return json.dumps(payloads, indent=2)
    
    def log_message(self, format, *args):
        # Custom logging
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {args[0]}")

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, APIHandler)
    print("=" * 70)
    print("🚀 Intelligent Referral Management Platform - Demo Server")
    print("=" * 70)
    print(f"\n✓ Server running at: http://localhost:{port}")
    print(f"✓ API Documentation: http://localhost:{port}/docs")
    print(f"✓ Test Payloads: http://localhost:{port}/payloads")
    print(f"✓ Health Check: http://localhost:{port}/health")
    print("\n📊 All 4 AI Opportunities Available:")
    print("  1. Document Code Extraction - POST /api/v1/documents/analyze")
    print("  2. Specialist Recommendation - POST /api/v1/specialists/search")
    print("  3. Referral History Summary - GET /api/v1/patients/{id}/history")
    print("  4. Missing Document Detection - POST /api/v1/documents/check-completeness")
    print("\n🎯 Quick Test:")
    print(f"  curl http://localhost:{port}/payloads")
    print("\nPress Ctrl+C to stop")
    print("=" * 70)
    httpd.serve_forever()

if __name__ == '__main__':
    try:
        run_server(8000)
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")
