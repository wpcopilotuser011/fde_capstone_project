#!/bin/bash

# Quick Test Script for All AI Opportunities
# Run this to verify all 4 AI capabilities work

echo "======================================================================"
echo "🧪 Testing All 4 AI Opportunities"
echo "======================================================================"
echo ""

# Start demo server if not running
if ! pgrep -f "demo_server.py" > /dev/null; then
    echo "Starting demo server..."
    cd "/home/ubuntu/Capstone Assignment"
    nohup python3 demo_server.py > server.log 2>&1 &
    sleep 3
fi

echo "Server URL: http://localhost:8000"
echo ""

# Test 1: AI Opportunity #1 - Document Code Extraction
echo "1️⃣  AI #1: Document Code Extraction"
echo "======================================"
curl -s -X POST http://localhost:8000/api/v1/documents/analyze \
  -H "Content-Type: application/json" \
  -d '{"document_id": "DOC123", "analysis_type": "full"}' | python3 -m json.tool
echo ""
echo ""

# Test 2: AI Opportunity #2 - Specialist Recommendation
echo "2️⃣  AI #2: Specialist Recommendation"
echo "======================================"
curl -s -X POST http://localhost:8000/api/v1/specialists/search \
  -H "Content-Type: application/json" \
  -d '{"specialty": "Cardiology", "diagnosis_codes": ["I10"], "insurance_provider": "Blue Cross"}' | python3 -m json.tool
echo ""
echo ""

# Test 3: AI Opportunity #3 - Referral History Summary
echo "3️⃣  AI #3: Referral History Summary"
echo "======================================"
curl -s http://localhost:8000/api/v1/patients/PT001/history | python3 -m json.tool
echo ""
echo ""

# Test 4: AI Opportunity #4 - Missing Document Detection
echo "4️⃣  AI #4: Missing Document Detection"
echo "======================================"
curl -s -X POST "http://localhost:8000/api/v1/documents/check-completeness?specialty=Cardiology" \
  -H "Content-Type: application/json" \
  -d '{"documents": ["referral_form"]}' | python3 -m json.tool
echo ""
echo ""

# Test 5: Complete Demo Workflow
echo "5️⃣  Complete Demo Workflow (All AI Opportunities)"
echo "======================================"
curl -s -X POST http://localhost:8000/api/v1/demo/process-referral | python3 -m json.tool
echo ""
echo ""

echo "======================================================================"
echo "✅ All Tests Complete!"
echo "======================================================================"
echo ""
echo "📋 Summary:"
echo "  • All 4 AI Opportunities tested"
echo "  • Server running at: http://localhost:8000"
echo "  • API Docs: http://localhost:8000/docs"
echo "  • Test Payloads: http://localhost:8000/payloads"
echo ""
echo "See TEST_PAYLOADS.md for detailed test instructions"
echo "======================================================================"
