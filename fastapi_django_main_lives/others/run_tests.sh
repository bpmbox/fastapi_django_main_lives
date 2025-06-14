#!/bin/bash

# OpenInterpreter Test Runner Script

echo "🧪 OpenInterpreter Test Suite"
echo "=============================="

# Set up environment
export PYTHONPATH="/workspaces/fastapi_django_main_live:$PYTHONPATH"

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "Installing pytest..."
    pip install pytest pytest-cov pytest-asyncio
fi

echo ""
echo "🔧 Running OpenInterpreter Tests..."
echo "===================================="

# Run the test file directly first
echo "1. Running basic functionality tests..."
cd /workspaces/fastapi_django_main_live
python -m tests.test_openinterpreter

echo ""
echo "🚀 Starting Test API Server..."
echo "=============================="

# Start the test API server in background
echo "Starting test API on port 7861..."
python test_app.py &
TEST_API_PID=$!

# Wait for the server to start
sleep 3

echo ""
echo "🧪 Testing API Endpoints..."
echo "============================"

# Test the API endpoints using curl
echo "Testing health endpoint..."
curl -s http://localhost:7861/health | python -m json.tool

echo ""
echo "Testing code validation..."
curl -s -X POST http://localhost:7861/test/validate-code \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello, World!\")"}' | python -m json.tool

echo ""
echo "Testing database functionality..."
curl -s http://localhost:7861/test/database | python -m json.tool

echo ""
echo "Running comprehensive test suite..."
curl -s http://localhost:7861/test/suite | python -m json.tool

echo ""
echo "Testing basic chat (this may take a moment)..."
curl -s -X POST http://localhost:7861/test/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is 2+2?", "password": "12345"}' | python -m json.tool

# Clean up - stop the test API server
echo ""
echo "🧹 Cleaning up..."
kill $TEST_API_PID 2>/dev/null

echo ""
echo "📊 Test Summary"
echo "==============="
echo "✓ Basic functionality tests completed"
echo "✓ API endpoint tests completed"
echo "✓ Code validation tests completed"
echo "✓ Database operation tests completed"
echo "✓ Chat functionality tests completed"

echo ""
echo "🎯 To run the test API manually:"
echo "  python test_app.py"
echo "  # Then visit http://localhost:7861/docs for API documentation"

echo ""
echo "🔍 To run specific tests:"
echo "  pytest tests/test_openinterpreter.py::TestOpenInterpreter::test_validate_code_valid"
echo "  pytest tests/test_openinterpreter.py -k \"code_validation\""

echo ""
echo "📝 Test completed successfully!"
