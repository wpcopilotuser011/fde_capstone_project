"""
MCP Server for Specialist Recommendation
AI Opportunity #2: Recommend specialists based on diagnosis, location, and insurance network
"""
import json
import asyncio
from typing import Any, List, Dict
from mcp.server import Server
from mcp.types import Tool, TextContent
from datetime import datetime, timedelta
import random


class SpecialistRecommender:
    """Recommends specialists based on multiple criteria using AI"""
    
    def __init__(self):
        # Mock specialist database
        self.specialists = self._load_specialists()
    
    def _load_specialists(self) -> List[Dict]:
        """Load specialist database (mocked)"""
        return [
            {
                "provider_id": "PROV001",
                "name": "Dr. Sarah Johnson",
                "specialty": "Cardiology",
                "sub_specialties": ["interventional cardiology", "heart failure"],
                "location": {"city": "Boston", "state": "MA", "zip": "02115"},
                "coordinates": {"lat": 42.3601, "lon": -71.0589},
                "insurance_networks": ["Blue Cross", "Aetna", "UnitedHealth"],
                "npi": "1234567890",
                "rating": 4.8,
                "years_experience": 15,
                "accepts_new_patients": True,
                "next_available": "2026-08-15"
            },
            {
                "provider_id": "PROV002",
                "name": "Dr. Michael Chen",
                "specialty": "Orthopedics",
                "sub_specialties": ["sports medicine", "shoulder surgery"],
                "location": {"city": "Boston", "state": "MA", "zip": "02120"},
                "coordinates": {"lat": 42.3355, "lon": -71.1005},
                "insurance_networks": ["Blue Cross", "Cigna", "Medicare"],
                "npi": "1234567891",
                "rating": 4.9,
                "years_experience": 20,
                "accepts_new_patients": True,
                "next_available": "2026-08-12"
            },
            {
                "provider_id": "PROV003",
                "name": "Dr. Emily Rodriguez",
                "specialty": "Neurology",
                "sub_specialties": ["stroke", "headache disorders"],
                "location": {"city": "Cambridge", "state": "MA", "zip": "02139"},
                "coordinates": {"lat": 42.3736, "lon": -71.1097},
                "insurance_networks": ["Aetna", "UnitedHealth", "Medicaid"],
                "npi": "1234567892",
                "rating": 4.7,
                "years_experience": 12,
                "accepts_new_patients": True,
                "next_available": "2026-08-18"
            },
            {
                "provider_id": "PROV004",
                "name": "Dr. James Williams",
                "specialty": "Cardiology",
                "sub_specialties": ["electrophysiology", "arrhythmia"],
                "location": {"city": "Boston", "state": "MA", "zip": "02114"},
                "coordinates": {"lat": 42.3625, "lon": -71.0686},
                "insurance_networks": ["Blue Cross", "Harvard Pilgrim", "Tufts"],
                "npi": "1234567893",
                "rating": 4.9,
                "years_experience": 18,
                "accepts_new_patients": True,
                "next_available": "2026-08-20"
            }
        ]
    
    def _calculate_distance(self, coord1: dict, coord2: dict) -> float:
        """Calculate approximate distance between two coordinates (simplified)"""
        # Simplified distance calculation (in real app, use haversine formula)
        lat_diff = abs(coord1["lat"] - coord2["lat"])
        lon_diff = abs(coord1["lon"] - coord2["lon"])
        return ((lat_diff ** 2 + lon_diff ** 2) ** 0.5) * 69  # Approximate miles
    
    async def recommend_specialists(
        self,
        diagnosis_codes: List[str],
        specialty: str,
        insurance_provider: str = None,
        patient_location: dict = None,
        max_distance: float = 50.0,
        urgency: str = "routine"
    ) -> List[Dict]:
        """
        Recommend specialists using AI-powered matching
        Considers: specialty match, insurance network, location, availability, ratings
        """
        # Filter by specialty
        candidates = [s for s in self.specialists if s["specialty"].lower() == specialty.lower()]
        
        # Filter by insurance if provided
        if insurance_provider:
            candidates = [
                s for s in candidates 
                if insurance_provider in s["insurance_networks"]
            ]
        
        # Calculate match scores
        recommendations = []
        for specialist in candidates:
            score = 0.0
            reasons = []
            
            # Base specialty match
            score += 0.3
            reasons.append(f"Specialty match: {specialty}")
            
            # Insurance network match
            if insurance_provider and insurance_provider in specialist["insurance_networks"]:
                score += 0.2
                reasons.append(f"In-network for {insurance_provider}")
            
            # Rating factor
            rating_score = (specialist["rating"] / 5.0) * 0.2
            score += rating_score
            reasons.append(f"High rating: {specialist['rating']}/5.0")
            
            # Experience factor
            exp_score = min(specialist["years_experience"] / 20.0, 1.0) * 0.15
            score += exp_score
            
            # Availability factor
            next_avail = datetime.strptime(specialist["next_available"], "%Y-%m-%d")
            days_wait = (next_avail - datetime.now()).days
            
            if urgency == "emergent" and days_wait <= 3:
                score += 0.15
                reasons.append("Available within 3 days for emergent case")
            elif urgency == "urgent" and days_wait <= 7:
                score += 0.15
                reasons.append("Available within 1 week for urgent case")
            elif days_wait <= 14:
                score += 0.10
                reasons.append("Available within 2 weeks")
            
            # Location proximity (if patient location provided)
            distance = None
            if patient_location and "coordinates" in patient_location:
                distance = self._calculate_distance(
                    specialist["coordinates"],
                    patient_location["coordinates"]
                )
                if distance <= max_distance:
                    proximity_score = (1 - (distance / max_distance)) * 0.1
                    score += proximity_score
                    reasons.append(f"Located {distance:.1f} miles away")
            
            recommendations.append({
                "provider": specialist,
                "match_score": round(score, 2),
                "distance_miles": round(distance, 1) if distance else None,
                "next_available": specialist["next_available"],
                "reasons": reasons,
                "wait_time_days": days_wait
            })
        
        # Sort by match score
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        
        return recommendations[:5]  # Return top 5
    
    async def suggest_alternatives(
        self,
        original_provider_id: str,
        wait_time_threshold: int = 14
    ) -> List[Dict]:
        """
        AI Opportunity #7: Suggest alternative providers if appointments exceed target wait times
        """
        # Find original provider
        original = next((s for s in self.specialists if s["provider_id"] == original_provider_id), None)
        
        if not original:
            return []
        
        # Check wait time
        next_avail = datetime.strptime(original["next_available"], "%Y-%m-%d")
        days_wait = (next_avail - datetime.now()).days
        
        if days_wait <= wait_time_threshold:
            return []  # No alternatives needed
        
        # Find alternatives with same specialty and better availability
        alternatives = []
        for specialist in self.specialists:
            if (specialist["provider_id"] != original_provider_id and
                specialist["specialty"] == original["specialty"]):
                
                alt_avail = datetime.strptime(specialist["next_available"], "%Y-%m-%d")
                alt_wait = (alt_avail - datetime.now()).days
                
                if alt_wait < days_wait:
                    alternatives.append({
                        "provider": specialist,
                        "wait_time_days": alt_wait,
                        "time_saved_days": days_wait - alt_wait,
                        "reason": f"Available {days_wait - alt_wait} days sooner"
                    })
        
        alternatives.sort(key=lambda x: x["wait_time_days"])
        return alternatives[:3]


# Initialize MCP Server
app = Server("specialist-recommender")
recommender = SpecialistRecommender()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="recommend_specialists",
            description="AI-powered specialist recommendation based on diagnosis, location, insurance, and availability",
            inputSchema={
                "type": "object",
                "properties": {
                    "diagnosis_codes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of ICD-10 diagnosis codes"
                    },
                    "specialty": {
                        "type": "string",
                        "description": "Required specialty (e.g., Cardiology, Orthopedics)"
                    },
                    "insurance_provider": {
                        "type": "string",
                        "description": "Patient's insurance provider"
                    },
                    "patient_location": {
                        "type": "object",
                        "description": "Patient's location with coordinates"
                    },
                    "urgency": {
                        "type": "string",
                        "enum": ["routine", "urgent", "emergent"],
                        "description": "Urgency level"
                    }
                },
                "required": ["diagnosis_codes", "specialty"]
            }
        ),
        Tool(
            name="suggest_alternative_providers",
            description="Suggest alternative providers if wait time exceeds threshold",
            inputSchema={
                "type": "object",
                "properties": {
                    "provider_id": {
                        "type": "string",
                        "description": "Original provider ID"
                    },
                    "wait_time_threshold": {
                        "type": "integer",
                        "description": "Maximum acceptable wait time in days"
                    }
                },
                "required": ["provider_id"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    
    if name == "recommend_specialists":
        result = await recommender.recommend_specialists(
            diagnosis_codes=arguments["diagnosis_codes"],
            specialty=arguments["specialty"],
            insurance_provider=arguments.get("insurance_provider"),
            patient_location=arguments.get("patient_location"),
            urgency=arguments.get("urgency", "routine")
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "suggest_alternative_providers":
        result = await recommender.suggest_alternatives(
            original_provider_id=arguments["provider_id"],
            wait_time_threshold=arguments.get("wait_time_threshold", 14)
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
