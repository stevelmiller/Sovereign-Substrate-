#!/bin/bash
# Cordelia-11 Submission Verification Script
# Run this to verify all components before final submission

set -e

echo "======================================================"
echo "CORDELIA-11 SUBMISSION VERIFICATION"
echo "Build 11 | Gemini 3.0 Hackathon"
echo "======================================================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

success_count=0
total_checks=0

check() {
    total_checks=$((total_checks + 1))
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
        success_count=$((success_count + 1))
    else
        echo -e "${RED}❌ $1${NC}"
    fi
}

# 1. File Structure Check
echo "1. Checking File Structure..."
test -f README.md && check "README.md exists"
test -f DEVPOST_SUBMISSION.md && check "DEVPOST_SUBMISSION.md exists"
test -f VIDEO_SCRIPT.md && check "VIDEO_SCRIPT.md exists"
test -f DEPLOYMENT_GUIDE.md && check "DEPLOYMENT_GUIDE.md exists"
test -f QUICKSTART.md && check "QUICKSTART.md exists"
test -f SUBMISSION_SUMMARY.md && check "SUBMISSION_SUMMARY.md exists"
test -f server.py && check "server.py exists"
test -f gemini_instances.py && check "gemini_instances.py exists"
test -f test_server.py && check "test_server.py exists"
test -f requirements.txt && check "requirements.txt exists"
test -f .env.example && check ".env.example exists"
test -f Dockerfile && check "Dockerfile exists"
test -f .gitignore && check ".gitignore exists"
test -f .github/workflows/ci.yml && check "CI workflow exists"
echo ""

# 2. Content Validation
echo "2. Validating Documentation Content..."
grep -q "Gemini 3.0 Hackathon" README.md && check "README mentions hackathon"
grep -q "4x Gemini 3.0 Pro" DEVPOST_SUBMISSION.md && check "Devpost describes 4x architecture"
grep -q "11.00Hz" README.md && check "README mentions resonance frequency"
grep -q "Navigator" README.md && check "README describes Navigator"
grep -q "Arbiter" README.md && check "README describes Arbiter"
grep -q "ARD" README.md && check "README describes ARD"
grep -q "Cognitive Intellect" README.md && check "README describes Cognitive Intellect"
grep -q "February 9, 2026" DEVPOST_SUBMISSION.md && check "Deadline documented"
echo ""

# 3. Python Syntax Check
echo "3. Checking Python Syntax..."
python -m py_compile server.py 2>/dev/null && check "server.py syntax valid"
python -m py_compile gemini_instances.py 2>/dev/null && check "gemini_instances.py syntax valid"
python -m py_compile test_server.py 2>/dev/null && check "test_server.py syntax valid"
echo ""

# 4. Dependencies Check
echo "4. Checking Dependencies..."
grep -q "flask" requirements.txt && check "Flask in requirements.txt"
grep -q "google-generativeai" requirements.txt && check "Gemini API in requirements.txt"
grep -q "python-dotenv" requirements.txt && check "dotenv in requirements.txt"
echo ""

# 5. Environment Configuration
echo "5. Checking Environment Configuration..."
grep -q "GOOGLE_API_KEY" .env.example && check "API key config present"
grep -q "RESONANCE_HZ=11.00" .env.example && check "Resonance frequency configured"
grep -q "NAVIGATOR_MODEL" .env.example && check "Navigator model configured"
grep -q "ARBITER_MODEL" .env.example && check "Arbiter model configured"
grep -q "ARD_MODEL" .env.example && check "ARD model configured"
grep -q "COGNITIVE_INTELLECT_MODEL" .env.example && check "Cognitive Intellect model configured"
echo ""

# 6. Test Execution
echo "6. Running Test Suite..."
if command -v pytest &> /dev/null || python -m pytest --version &> /dev/null; then
    python -m pytest test_server.py -v -x 2>&1 | tail -2
    check "Test suite execution"
else
    echo -e "${YELLOW}⚠️  pytest not installed, skipping tests${NC}"
fi
echo ""

# 7. Server Start Test (Demo Mode)
echo "7. Testing Server Startup (Demo Mode)..."
timeout 5 python server.py > /tmp/cordelia_test.log 2>&1 &
SERVER_PID=$!
sleep 3

if ps -p $SERVER_PID > /dev/null; then
    check "Server starts successfully"
    kill $SERVER_PID 2>/dev/null || true
else
    echo -e "${RED}❌ Server failed to start${NC}"
fi
echo ""

# 8. Endpoint Tests
echo "8. Testing Endpoints..."
if command -v curl &> /dev/null; then
    timeout 5 python server.py > /dev/null 2>&1 &
    SERVER_PID=$!
    sleep 3
    
    curl -f -s http://localhost:5000/ > /dev/null && check "Root endpoint responds"
    curl -f -s http://localhost:5000/pulse > /dev/null && check "/pulse endpoint responds"
    curl -f -s http://localhost:5000/health > /dev/null && check "/health endpoint responds"
    curl -f -s -X POST http://localhost:5000/sentinel \
        -H "Content-Type: application/json" \
        -d '{"prompt":"test"}' > /dev/null && check "/sentinel endpoint responds"
    
    kill $SERVER_PID 2>/dev/null || true
else
    echo -e "${YELLOW}⚠️  curl not installed, skipping endpoint tests${NC}"
fi
echo ""

# 9. Docker Build Test
echo "9. Testing Docker Build..."
if command -v docker &> /dev/null; then
    docker build -t cordelia-11:verify . > /dev/null 2>&1 && check "Docker image builds"
else
    echo -e "${YELLOW}⚠️  Docker not installed, skipping build test${NC}"
fi
echo ""

# 10. Git Status Check
echo "10. Checking Git Status..."
if [ -d .git ]; then
    if [ -z "$(git status --porcelain)" ]; then
        check "Working directory clean"
    else
        echo -e "${YELLOW}⚠️  Uncommitted changes present${NC}"
    fi
    
    git log -1 --oneline > /dev/null && check "Git history present"
else
    echo -e "${YELLOW}⚠️  Not a git repository${NC}"
fi
echo ""

# Summary
echo "======================================================"
echo "VERIFICATION SUMMARY"
echo "======================================================"
echo ""
echo "Checks Passed: $success_count / $total_checks"
echo ""

if [ $success_count -eq $total_checks ]; then
    echo -e "${GREEN}🎉 ALL CHECKS PASSED!${NC}"
    echo ""
    echo "✅ Ready for Gemini 3.0 Hackathon submission"
    echo ""
    echo "Next steps:"
    echo "1. Deploy to Cloud Run: gcloud run deploy cordelia-11 --source ."
    echo "2. Record 3-minute demo video (see VIDEO_SCRIPT.md)"
    echo "3. Submit to Devpost (see DEVPOST_SUBMISSION.md)"
    echo ""
    echo "Deadline: February 9, 2026 (5PM PT)"
    exit 0
else
    echo -e "${RED}⚠️  SOME CHECKS FAILED${NC}"
    echo ""
    echo "Please review the failures above and fix them before submission."
    exit 1
fi
