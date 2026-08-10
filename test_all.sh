#!/bin/bash

# Comprehensive Test Script for Referral Management Platform
# Tests all 4 AI opportunities and core functionality

echo "🧪 Testing Referral Management Platform"
echo "========================================"
echo ""

BASE_URL="http://localhost:8000"
FAILED=0
PASSED=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to test endpoint
test_endpoint() {
    local name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    
    echo -n "Testing: $name... "
    
    if [ "$method" == "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$BASE_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✓ PASSED${NC} (HTTP $http_code)"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC} (HTTP $http_code)"
        echo "Response: $body"
        ((FAILED++))
        return 1
    fi
}

# Test 1: Health Check
echo "1️⃣  Basic Health Checks"
echo "----------------------"
test_endpoint "Health endpoint" "GET" "/health" ""
test_endpoint "Root endpoint" "GET" "/" ""
echo ""

# Test 2: AI Opportunity #1 - Document Code Extraction
echo "2️⃣  AI Opportunity #1: Document Code Extraction"
echo "------------------------------------------------"
test_endpoint "Analyze document" "POST" "/api/v1/documents/analyze" '{
  "document_id": "DOC123",
  "analysis_type": "full"
}'
echo ""

# Test 3: AI Opportunity #2 - Specialist Recommendation
echo "3️⃣  AI Opportunity #2: Specialist Recommendation"
echo "-------------------------------------------------"
test_endpoint "Search specialists" "POST" "/api/v1/specialists/search" '{
  "specialty": "Cardiology",
  "diagnosis_codes": ["I10"],
  "insurance_provider": "Blue Cross"
}'
echo ""

# Test 4: AI Opportunity #3 - Referral History Summary
echo "4️⃣  AI Opportunity #3: Referral History Summary"
echo "------------------------------------------------"
test_endpoint "Get patient history" "GET" "/api/v1/patients/PT001/history" ""
echo ""

# Test 5: AI Opportunity #4 - Missing Document Detection
echo "5️⃣  AI Opportunity #4: Missing Document Detection"
echo "--------------------------------------------------"
test_endpoint "Check document completeness" "POST" "/api/v1/documents/check-completeness?specialty=Cardiology" '{
  "documents": ["referral_form"]
}'
echo ""

# Test 6: Conversational AI (Bonus - AI Opportunity #6)
echo "6️⃣  AI Opportunity #6: Conversational Assistant"
echo "------------------------------------------------"
test_endpoint "Conversational AI" "POST" "/api/v1/conversation" '{
  "user_id": "PT001",
  "message": "What is the status of my referral?"
}'
echo ""

# Test 7: Complete Referral Workflow
echo "7️⃣  Complete Referral Workflow"
echo "-------------------------------"
test_endpoint "Submit referral" "POST" "/api/v1/referrals" '{
  "patient": {
    "patient_id": "PT_TEST_001",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1980-01-01",
    "insurance_id": "INS001",
    "insurance_provider": "Blue Cross"
  },
  "referring_provider_id": "DR001",
  "specialty_requested": "Cardiology",
  "diagnosis_codes": ["I10"],
  "clinical_summary": "Test referral",
  "priority": "routine"
}'

test_endpoint "Check eligibility" "POST" "/api/v1/eligibility" '{
  "patient_id": "PT001",
  "insurance_id": "INS001",
  "insurance_provider": "Blue Cross",
  "service_type": "specialist_visit"
}'
echo ""

# Test 8: Demo Endpoint
echo "8️⃣  Complete Demo Workflow"
echo "---------------------------"
test_endpoint "Demo workflow" "POST" "/api/v1/demo/process-referral" ""
echo ""

# Summary
echo "========================================"
echo "📊 Test Summary"
echo "========================================"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo "Total:  $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    echo ""
    echo "🎉 The platform is working correctly!"
    echo "All 4 AI opportunities are functional."
    exit 0
else
    echo -e "${RED}❌ Some tests failed!${NC}"
    echo ""
    echo "Please check the application logs:"
    echo "  docker-compose logs -f"
    echo "  tail -f logs/application.log"
    exit 1
fi
