"""
MCP Server for Conversational AI Assistant
AI Opportunity #6: Answer patient queries through a conversational assistant
AI Opportunity #3: Summarise referral history for specialists before consultation
"""
import json
import asyncio
from typing import Any, List, Dict, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
from datetime import datetime


class ConversationalAssistant:
    """AI-powered conversational assistant for patient queries and referral support"""
    
    def __init__(self):
        self.conversation_history = {}
        # Mock referral database for history
        self.referral_history = self._load_mock_history()
    
    def _load_mock_history(self) -> Dict:
        """Load mock referral history"""
        return {
            "PT001": [
                {
                    "referral_id": "REF001",
                    "date": "2025-12-10",
                    "specialty": "Cardiology",
                    "diagnosis": "Hypertension",
                    "status": "completed",
                    "provider": "Dr. Sarah Johnson",
                    "outcome": "Blood pressure controlled with medication"
                },
                {
                    "referral_id": "REF002",
                    "date": "2026-03-15",
                    "specialty": "Endocrinology",
                    "diagnosis": "Type 2 Diabetes",
                    "status": "completed",
                    "provider": "Dr. Amanda Lee",
                    "outcome": "Started on metformin, HbA1c improved to 6.8%"
                }
            ],
            "PT002": [
                {
                    "referral_id": "REF003",
                    "date": "2026-05-20",
                    "specialty": "Orthopedics",
                    "diagnosis": "Right shoulder pain",
                    "status": "completed",
                    "provider": "Dr. Michael Chen",
                    "outcome": "Physical therapy recommended, improving"
                }
            ]
        }
    
    async def handle_query(
        self,
        user_id: str,
        message: str,
        session_id: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Handle conversational queries from patients
        Uses AI to understand intent and provide relevant information
        """
        # Initialize session if needed
        if not session_id:
            session_id = f"session_{user_id}_{datetime.now().timestamp()}"
        
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        
        # Add message to history
        self.conversation_history[session_id].append({
            "role": "user",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Analyze intent (simplified - in production use actual LLM)
        intent = self._detect_intent(message)
        
        # Generate response based on intent
        response = await self._generate_response(intent, message, user_id, context)
        
        # Add response to history
        self.conversation_history[session_id].append({
            "role": "assistant",
            "message": response["message"],
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "session_id": session_id,
            "message": response["message"],
            "intent": intent,
            "suggestions": response.get("suggestions", []),
            "actions": response.get("actions", [])
        }
    
    def _detect_intent(self, message: str) -> str:
        """Detect user intent from message (simplified)"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["status", "where", "track", "update"]):
            return "check_status"
        elif any(word in message_lower for word in ["schedule", "appointment", "when", "book"]):
            return "schedule_appointment"
        elif any(word in message_lower for word in ["specialist", "doctor", "recommend", "who"]):
            return "find_specialist"
        elif any(word in message_lower for word in ["document", "upload", "form", "paperwork"]):
            return "document_help"
        elif any(word in message_lower for word in ["insurance", "coverage", "eligible", "pay"]):
            return "insurance_question"
        elif any(word in message_lower for word in ["help", "how", "what", "explain"]):
            return "general_help"
        else:
            return "general_query"
    
    async def _generate_response(
        self,
        intent: str,
        message: str,
        user_id: str,
        context: Optional[Dict]
    ) -> Dict:
        """Generate response based on intent"""
        
        responses = {
            "check_status": {
                "message": "I can help you check your referral status. Based on your recent referral, "
                          "you've been referred to Dr. Sarah Johnson (Cardiology). Your appointment is "
                          "scheduled for August 15, 2026 at 2:00 PM. Your insurance eligibility has been "
                          "verified and you're all set!",
                "suggestions": [
                    "Get directions to the appointment",
                    "Reschedule appointment",
                    "View required documents"
                ],
                "actions": ["status_checked"]
            },
            "schedule_appointment": {
                "message": "I'd be happy to help you schedule your appointment. Based on your referral to "
                          "Cardiology, I've found Dr. Sarah Johnson who has availability on August 15 at "
                          "2:00 PM or August 18 at 10:00 AM. Which time works better for you?",
                "suggestions": [
                    "Book August 15 at 2:00 PM",
                    "Book August 18 at 10:00 AM",
                    "See more available times"
                ],
                "actions": ["appointment_search_initiated"]
            },
            "find_specialist": {
                "message": "I can help you find the right specialist. Based on your diagnosis of hypertension "
                          "and diabetes, I recommend Dr. Sarah Johnson, a cardiologist with 15 years of "
                          "experience. She accepts your insurance (Blue Cross) and has excellent ratings "
                          "(4.8/5). She's located 3.2 miles from you.",
                "suggestions": [
                    "View Dr. Johnson's full profile",
                    "See other cardiologists",
                    "Schedule with Dr. Johnson"
                ],
                "actions": ["specialist_recommended"]
            },
            "document_help": {
                "message": "For your cardiology referral, you'll need the following documents:\n"
                          "✓ Referral form (uploaded)\n"
                          "✓ Insurance card (uploaded)\n"
                          "⚠ Clinical notes (missing)\n"
                          "⚠ Recent lab results (missing)\n\n"
                          "Please upload the missing documents to complete your referral.",
                "suggestions": [
                    "Upload clinical notes",
                    "Upload lab results",
                    "View document requirements"
                ],
                "actions": ["document_check_completed"]
            },
            "insurance_question": {
                "message": "Good news! Your insurance (Blue Cross Blue Shield) has been verified and you're "
                          "eligible for the cardiology specialist visit. Your copay will be $40, and no "
                          "prior authorization is required for this referral.",
                "suggestions": [
                    "View full coverage details",
                    "Check deductible status",
                    "Find in-network providers"
                ],
                "actions": ["insurance_verified"]
            },
            "general_help": {
                "message": "I'm here to help with your referral! I can assist you with:\n"
                          "• Checking your referral status\n"
                          "• Scheduling appointments with specialists\n"
                          "• Finding the right specialist for your needs\n"
                          "• Uploading and managing documents\n"
                          "• Answering insurance and coverage questions\n\n"
                          "What would you like help with?",
                "suggestions": [
                    "Check my referral status",
                    "Schedule an appointment",
                    "Upload documents"
                ],
                "actions": []
            },
            "general_query": {
                "message": "I understand you have a question about your referral. Let me help you with that. "
                          "Could you please provide more details about what you'd like to know?",
                "suggestions": [
                    "Check referral status",
                    "Find a specialist",
                    "Schedule appointment"
                ],
                "actions": []
            }
        }
        
        return responses.get(intent, responses["general_query"])
    
    async def summarize_referral_history(
        self,
        patient_id: str,
        include_outcomes: bool = True
    ) -> Dict:
        """
        AI Opportunity #3: Summarise referral history for specialists before consultation
        Generate comprehensive summary of patient's referral history
        """
        history = self.referral_history.get(patient_id, [])
        
        if not history:
            return {
                "patient_id": patient_id,
                "summary": "No previous referral history available.",
                "referral_count": 0,
                "specialties_visited": [],
                "common_diagnoses": [],
                "risk_factors": []
            }
        
        # Analyze history
        specialties = list(set([ref["specialty"] for ref in history]))
        diagnoses = [ref["diagnosis"] for ref in history]
        
        # Generate AI summary (simplified - in production use actual LLM)
        summary_parts = [
            f"Patient has {len(history)} previous referrals on record.",
            f"Specialties visited: {', '.join(specialties)}.",
            f"Primary diagnoses: {', '.join(set(diagnoses))}."
        ]
        
        if include_outcomes:
            completed = [r for r in history if r["status"] == "completed"]
            if completed:
                summary_parts.append(
                    f"Previous referrals show good patient compliance with {len(completed)} completed visits."
                )
        
        # Identify patterns and risk factors
        risk_factors = []
        if "Hypertension" in diagnoses and "Type 2 Diabetes" in diagnoses:
            risk_factors.append("Cardiovascular risk factors present (HTN + DM)")
        
        summary = " ".join(summary_parts)
        
        return {
            "patient_id": patient_id,
            "summary": summary,
            "referral_count": len(history),
            "specialties_visited": specialties,
            "common_diagnoses": list(set(diagnoses)),
            "risk_factors": risk_factors,
            "recent_referrals": history[-3:],  # Last 3 referrals
            "detailed_history": history if include_outcomes else None
        }


# Initialize MCP Server
app = Server("conversational-assistant")
assistant = ConversationalAssistant()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="handle_patient_query",
            description="AI conversational assistant to answer patient queries about referrals, appointments, and status",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "Patient or user ID"
                    },
                    "message": {
                        "type": "string",
                        "description": "User's question or message"
                    },
                    "session_id": {
                        "type": "string",
                        "description": "Optional session ID for conversation continuity"
                    },
                    "context": {
                        "type": "object",
                        "description": "Optional context about current referral or patient state"
                    }
                },
                "required": ["user_id", "message"]
            }
        ),
        Tool(
            name="summarize_patient_history",
            description="Generate AI-powered summary of patient's referral history for specialist review",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "string",
                        "description": "Patient ID"
                    },
                    "include_outcomes": {
                        "type": "boolean",
                        "description": "Include outcomes and detailed information"
                    }
                },
                "required": ["patient_id"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    
    if name == "handle_patient_query":
        result = await assistant.handle_query(
            user_id=arguments["user_id"],
            message=arguments["message"],
            session_id=arguments.get("session_id"),
            context=arguments.get("context")
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "summarize_patient_history":
        result = await assistant.summarize_referral_history(
            patient_id=arguments["patient_id"],
            include_outcomes=arguments.get("include_outcomes", True)
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the MCP server"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
