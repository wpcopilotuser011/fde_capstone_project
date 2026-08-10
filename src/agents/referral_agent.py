"""
AI Agent Orchestration using LangGraph
Coordinates multiple AI agents to handle referral workflow
"""
from typing import TypedDict, Annotated, Sequence, List, Dict, Any
from langraph.graph import Graph, StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
import json
import os
from datetime import datetime


class ReferralState(TypedDict):
    """State for referral processing workflow"""
    referral_id: str
    patient_id: str
    messages: Sequence[BaseMessage]
    documents: List[Dict]
    diagnosis_codes: List[Dict]
    procedure_codes: List[Dict]
    missing_documents: List[str]
    eligibility_status: Dict
    recommended_specialists: List[Dict]
    selected_specialist: Dict
    appointment: Dict
    current_step: str
    errors: List[str]
    completed_steps: List[str]


class ReferralAgent:
    """Main agent for orchestrating referral workflow"""
    
    def __init__(self, model_name: str = "gpt-4", api_key: str = None, api_base: str = None):
        """Initialize the agent with LLM"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.api_base = api_base or os.getenv("OPENAI_API_BASE")
        
        # Initialize LLM - use ChatOpenAI for Bedrock compatibility
        llm_config = {
            "model": model_name,
            "temperature": 0.7,
            "api_key": self.api_key
        }
        
        # Add base_url if provided (for Bedrock/custom endpoints)
        if self.api_base:
            llm_config["base_url"] = self.api_base
        
        self.llm = ChatOpenAI(**llm_config)
        
        # Build workflow graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the referral processing workflow using LangGraph"""
        
        workflow = StateGraph(ReferralState)
        
        # Add nodes for each step
        workflow.add_node("analyze_documents", self.analyze_documents)
        workflow.add_node("check_completeness", self.check_completeness)
        workflow.add_node("verify_eligibility", self.verify_eligibility)
        workflow.add_node("recommend_specialist", self.recommend_specialist)
        workflow.add_node("schedule_appointment", self.schedule_appointment)
        workflow.add_node("send_notifications", self.send_notifications)
        
        # Define workflow edges
        workflow.set_entry_point("analyze_documents")
        
        workflow.add_edge("analyze_documents", "check_completeness")
        workflow.add_conditional_edges(
            "check_completeness",
            self.should_continue_after_docs,
            {
                "continue": "verify_eligibility",
                "request_documents": END
            }
        )
        workflow.add_edge("verify_eligibility", "recommend_specialist")
        workflow.add_edge("recommend_specialist", "schedule_appointment")
        workflow.add_edge("schedule_appointment", "send_notifications")
        workflow.add_edge("send_notifications", END)
        
        return workflow.compile()
    
    async def analyze_documents(self, state: ReferralState) -> ReferralState:
        """
        Step 1: Analyze uploaded documents and extract codes
        Uses MCP document_processor server
        """
        print(f"[Agent] Analyzing documents for referral {state['referral_id']}")
        
        extracted_codes = []
        procedure_codes = []
        
        for doc in state.get("documents", []):
            # Simulate MCP call to document_processor
            # In production: use actual MCP client to call document_processor server
            result = {
                "diagnosis_codes": [
                    {"code": "I10", "system": "ICD-10", "description": "Essential hypertension"}
                ],
                "procedure_codes": [
                    {"code": "99213", "system": "CPT", "description": "Office visit"}
                ],
                "summary": "Patient referred for cardiology evaluation",
                "confidence": 0.90
            }
            
            extracted_codes.extend(result.get("diagnosis_codes", []))
            procedure_codes.extend(result.get("procedure_codes", []))
        
        state["diagnosis_codes"] = extracted_codes
        state["procedure_codes"] = procedure_codes
        state["completed_steps"].append("document_analysis")
        state["current_step"] = "check_completeness"
        
        # Add AI message
        state["messages"].append(
            AIMessage(content=f"Analyzed documents. Found {len(extracted_codes)} diagnosis codes.")
        )
        
        return state
    
    async def check_completeness(self, state: ReferralState) -> ReferralState:
        """
        Step 2: Check if all required documents are present
        Uses MCP document_processor server
        """
        print(f"[Agent] Checking document completeness for referral {state['referral_id']}")
        
        # Simulate MCP call to check_document_completeness
        result = {
            "complete": True,
            "missing_documents": [],
            "completeness_score": 1.0
        }
        
        # For demo, randomly mark some as incomplete
        if len(state.get("documents", [])) < 3:
            result = {
                "complete": False,
                "missing_documents": ["lab_results", "clinical_notes"],
                "completeness_score": 0.5
            }
        
        state["missing_documents"] = result.get("missing_documents", [])
        state["completed_steps"].append("completeness_check")
        state["current_step"] = "verify_eligibility"
        
        if result["missing_documents"]:
            state["messages"].append(
                AIMessage(content=f"Missing documents: {', '.join(result['missing_documents'])}")
            )
        else:
            state["messages"].append(
                AIMessage(content="All required documents are present.")
            )
        
        return state
    
    def should_continue_after_docs(self, state: ReferralState) -> str:
        """Decision: continue or request more documents"""
        if state.get("missing_documents"):
            return "request_documents"
        return "continue"
    
    async def verify_eligibility(self, state: ReferralState) -> ReferralState:
        """
        Step 3: Verify insurance eligibility
        Calls mock payer system
        """
        print(f"[Agent] Verifying eligibility for referral {state['referral_id']}")
        
        # Simulate eligibility check
        eligibility = {
            "eligible": True,
            "coverage_level": "Gold",
            "copay": 40.0,
            "prior_auth_required": False,
            "messages": ["Patient is eligible for specialist care"]
        }
        
        state["eligibility_status"] = eligibility
        state["completed_steps"].append("eligibility_verification")
        state["current_step"] = "recommend_specialist"
        
        state["messages"].append(
            AIMessage(content=f"Eligibility verified. Copay: ${eligibility['copay']}")
        )
        
        return state
    
    async def recommend_specialist(self, state: ReferralState) -> ReferralState:
        """
        Step 4: Recommend specialists based on criteria
        Uses MCP specialist_recommender server
        """
        print(f"[Agent] Recommending specialists for referral {state['referral_id']}")
        
        # Simulate MCP call to specialist_recommender
        recommendations = [
            {
                "provider": {
                    "provider_id": "PROV001",
                    "name": "Dr. Sarah Johnson",
                    "specialty": "Cardiology",
                    "rating": 4.8
                },
                "match_score": 0.92,
                "distance_miles": 3.2,
                "next_available": "2026-08-15",
                "reasons": ["Specialty match", "In-network", "High rating"]
            }
        ]
        
        state["recommended_specialists"] = recommendations
        state["selected_specialist"] = recommendations[0]["provider"]
        state["completed_steps"].append("specialist_recommendation")
        state["current_step"] = "schedule_appointment"
        
        state["messages"].append(
            AIMessage(content=f"Recommended specialist: {recommendations[0]['provider']['name']}")
        )
        
        return state
    
    async def schedule_appointment(self, state: ReferralState) -> ReferralState:
        """
        Step 5: Schedule appointment with specialist
        Calls mock scheduling system
        """
        print(f"[Agent] Scheduling appointment for referral {state['referral_id']}")
        
        # Simulate appointment scheduling
        appointment = {
            "appointment_id": f"APT{state['referral_id']}",
            "scheduled_time": "2026-08-15T14:00:00",
            "location": "123 Medical Center Dr",
            "status": "confirmed",
            "confirmation_sent": True
        }
        
        state["appointment"] = appointment
        state["completed_steps"].append("appointment_scheduling")
        state["current_step"] = "send_notifications"
        
        state["messages"].append(
            AIMessage(content=f"Appointment scheduled for {appointment['scheduled_time']}")
        )
        
        return state
    
    async def send_notifications(self, state: ReferralState) -> ReferralState:
        """
        Step 6: Send notifications to patient and providers
        """
        print(f"[Agent] Sending notifications for referral {state['referral_id']}")
        
        state["completed_steps"].append("notifications_sent")
        state["current_step"] = "completed"
        
        state["messages"].append(
            AIMessage(content="Notifications sent to patient and provider.")
        )
        
        return state
    
    async def process_referral(self, initial_state: Dict) -> ReferralState:
        """Process a referral through the complete workflow"""
        
        # Initialize state
        state: ReferralState = {
            "referral_id": initial_state["referral_id"],
            "patient_id": initial_state["patient_id"],
            "messages": [HumanMessage(content="Process new referral")],
            "documents": initial_state.get("documents", []),
            "diagnosis_codes": [],
            "procedure_codes": [],
            "missing_documents": [],
            "eligibility_status": {},
            "recommended_specialists": [],
            "selected_specialist": {},
            "appointment": {},
            "current_step": "start",
            "errors": [],
            "completed_steps": []
        }
        
        # Run workflow
        result = await self.workflow.ainvoke(state)
        
        return result


class ConversationalAgentOrchestrator:
    """
    Orchestrates conversational AI agents for multi-turn interactions
    """
    
    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name
        self.sessions = {}
    
    async def handle_conversation(
        self,
        user_id: str,
        message: str,
        session_id: str = None
    ) -> Dict:
        """Handle conversational interaction"""
        
        if not session_id:
            session_id = f"session_{user_id}_{datetime.now().timestamp()}"
        
        # Simulate MCP call to conversational_assistant
        response = {
            "session_id": session_id,
            "message": "I can help you with your referral. What would you like to know?",
            "intent": "general_query",
            "suggestions": [
                "Check referral status",
                "Find a specialist",
                "Schedule appointment"
            ]
        }
        
        return response


# Export agents
__all__ = ['ReferralAgent', 'ConversationalAgentOrchestrator']
