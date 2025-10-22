#!/bin/bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 REKRUTER AI BACKEND - COMPREHENSIVE AUDIT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Date: $(date)"
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "📊 1. PROJECT STATISTICS"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Files by type:"
find . -type f -name "*.py" | wc -l | xargs echo "  Python files:"
find . -type f -name "*.md" | wc -l | xargs echo "  Markdown docs:"
find . -type f -name "*.json" | wc -l | xargs echo "  JSON configs:"
find . -type f -name "*.yml" -o -name "*.yaml" | wc -l | xargs echo "  YAML configs:"
echo ""
echo "Lines of code:"
find . -name "*.py" -path "*/routers/*" -o -path "*/services/*" -o -name "models.py" -o -name "schemas.py" -o -name "config.py" -o -name "database.py" -o -name "main.py" | xargs wc -l 2>/dev/null | tail -1
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "📁 2. PROJECT STRUCTURE"
echo "═══════════════════════════════════════════════════════════"
tree -L 3 -I 'venv|__pycache__|*.pyc|.git|htmlcov|.pytest_cache|uploads|data|*.db' . 2>/dev/null || ls -la
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "🔌 3. API ENDPOINTS AUDIT"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Authentication endpoints:"
grep -r "^@router\." routers/auth.py 2>/dev/null | sed 's/@router\./  /' || echo "  ⚠️ No auth routes found"
echo ""
echo "Jobs endpoints:"
grep -r "^@router\." routers/jobs.py 2>/dev/null | sed 's/@router\./  /' || echo "  ⚠️ No job routes found"
echo ""
echo "Candidates endpoints:"
grep -r "^@router\." routers/candidates.py 2>/dev/null | sed 's/@router\./  /' || echo "  ⚠️ No candidate routes found"
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "🔐 4. SECURITY AUDIT"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "JWT Configuration:"
grep -E "SECRET_KEY|JWT_ALGORITHM|ACCESS_TOKEN" config.py 2>/dev/null | head -5 || echo "  ⚠️ Config not found"
echo ""
echo "Protected routes:"
grep -r "Depends(require_auth)" routers/*.py 2>/dev/null | wc -l | xargs echo "  Protected endpoints:"
grep -r "Depends(get_current" routers/*.py 2>/dev/null | wc -l | xargs echo "  Auth dependencies:"
echo ""
echo "Password hashing:"
grep -r "bcrypt\|passlib" services/auth.py requirements.txt 2>/dev/null | head -3
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "💾 5. DATABASE AUDIT"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Models defined:"
grep -E "^class.*\(Base\)" models.py 2>/dev/null | sed 's/class /  /' | sed 's/(Base)://' || echo "  ⚠️ No models found"
echo ""
echo "Migrations:"
ls -1 alembic/versions/*.py 2>/dev/null | wc -l | xargs echo "  Migration files:"
ls -lh alembic/versions/*.py 2>/dev/null | tail -1 | awk '{print "  Latest:", $9, "(" $5 ")"}'
echo ""
echo "Database config:"
grep -E "DATABASE_URL|SQLALCHEMY" config.py database.py 2>/dev/null | head -3
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "🧪 6. TESTING AUDIT"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Test files:"
ls -1 tests/test_*.py 2>/dev/null | wc -l | xargs echo "  Test modules:"
find tests/ -name "test_*.py" -exec grep -l "^def test_\|^async def test_" {} \; 2>/dev/null | wc -l | xargs echo "  Files with tests:"
echo ""
echo "Test functions:"
grep -r "^def test_\|^async def test_" tests/ 2>/dev/null | wc -l | xargs echo "  Total test functions:"
echo ""
echo "Coverage:"
if [ -f .coverage ]; then
  venv/bin/coverage report --skip-empty 2>/dev/null | tail -5
else
  echo "  ⚠️ No coverage data found"
fi
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "🤖 7. AI/ML SERVICES AUDIT"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Agent files:"
ls -lh services/agents/*.py 2>/dev/null | awk '{print "  " $9, "(" $5 ")"}' || echo "  ⚠️ No agents found"
echo ""
echo "LLM Integration:"
grep -E "ollama|claude|openai" services/llm_service.py config.py 2>/dev/null | head -3
echo ""
echo "RAG System:"
ls -lh services/rag_service.py 2>/dev/null | awk '{print "  " $9, "(" $5 ")"}' || echo "  ⚠️ No RAG service"
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "📦 8. DEPENDENCIES AUDIT"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Core dependencies:"
grep -E "fastapi|uvicorn|sqlalchemy|alembic|pydantic" requirements.txt 2>/dev/null || echo "  ⚠️ requirements.txt not found"
echo ""
echo "Security dependencies:"
grep -E "python-jose|passlib|bcrypt" requirements.txt 2>/dev/null
echo ""
echo "AI/ML dependencies:"
grep -E "anthropic|openai|langchain|ollama" requirements.txt 2>/dev/null
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "🐳 9. DOCKER AUDIT"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Docker files:"
ls -lh Dockerfile docker-compose.yml .dockerignore 2>/dev/null | awk '{print "  " $9, "(" $5 ")"}' || echo "  ⚠️ Docker files missing"
echo ""
echo "Docker status:"
docker ps 2>/dev/null | grep rekruter || echo "  ⚠️ No running containers"
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "📝 10. DOCUMENTATION AUDIT"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Documentation files:"
ls -lh *.md 2>/dev/null | awk '{print "  " $9, "(" $5 ")"}'
echo ""
echo "Frontend handoff:"
ls -lh ../frontend-handoff/ 2>/dev/null | grep -E "\\.md|\\.ts" | awk '{print "  " $9, "(" $5 ")"}'
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "⚠️  11. ISSUES & WARNINGS"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Checking for common issues..."
echo ""

# Check for hardcoded secrets
if grep -r "SECRET_KEY.*=.*['\"]" --include="*.py" . 2>/dev/null | grep -v "config.py" | grep -v "test_" >/dev/null; then
  echo "  ⚠️ WARNING: Hardcoded secrets found"
else
  echo "  ✅ No hardcoded secrets"
fi

# Check for TODO/FIXME
TODO_COUNT=$(grep -r "TODO\|FIXME" --include="*.py" . 2>/dev/null | wc -l)
echo "  ℹ️  TODO/FIXME comments: $TODO_COUNT"

# Check for print statements
PRINT_COUNT=$(grep -r "^[[:space:]]*print(" --include="*.py" . 2>/dev/null | grep -v "test_" | wc -l)
if [ "$PRINT_COUNT" -gt 0 ]; then
  echo "  ⚠️ WARNING: $PRINT_COUNT print() statements (should use logging)"
else
  echo "  ✅ No print() statements"
fi

# Check for missing __init__.py
MISSING_INIT=$(find . -type d -name "services" -o -name "routers" -o -name "middleware" | while read dir; do [ ! -f "$dir/__init__.py" ] && echo "$dir"; done)
if [ -n "$MISSING_INIT" ]; then
  echo "  ⚠️ WARNING: Missing __init__.py in: $MISSING_INIT"
else
  echo "  ✅ All __init__.py files present"
fi

echo ""

echo "═══════════════════════════════════════════════════════════"
echo "📊 12. PRODUCTION READINESS SCORE"
echo "═══════════════════════════════════════════════════════════"
echo ""

SCORE=0
MAX=100

# API Endpoints (20 points)
if [ -f "routers/jobs.py" ] && [ -f "routers/candidates.py" ] && [ -f "routers/auth.py" ]; then
  SCORE=$((SCORE + 20))
  echo "  ✅ API Endpoints: 20/20"
else
  echo "  ⚠️ API Endpoints: 0/20"
fi

# Authentication (15 points)
if grep -q "JWT" config.py 2>/dev/null && grep -q "bcrypt\|passlib" requirements.txt 2>/dev/null; then
  SCORE=$((SCORE + 15))
  echo "  ✅ Authentication: 15/15"
else
  echo "  ⚠️ Authentication: 0/15"
fi

# Database (15 points)
if [ -d "alembic/versions" ] && [ -f "models.py" ]; then
  SCORE=$((SCORE + 15))
  echo "  ✅ Database: 15/15"
else
  echo "  ⚠️ Database: 0/15"
fi

# Testing (10 points)
TEST_FILES=$(ls tests/test_*.py 2>/dev/null | wc -l)
if [ "$TEST_FILES" -ge 5 ]; then
  SCORE=$((SCORE + 10))
  echo "  ✅ Testing: 10/10"
else
  echo "  ⚠️ Testing: $((TEST_FILES * 2))/10"
  SCORE=$((SCORE + TEST_FILES * 2))
fi

# Docker (10 points)
if [ -f "Dockerfile" ] && [ -f "docker-compose.yml" ]; then
  SCORE=$((SCORE + 10))
  echo "  ✅ Docker: 10/10"
else
  echo "  ⚠️ Docker: 0/10"
fi

# Documentation (10 points)
DOC_FILES=$(ls *.md ../frontend-handoff/*.md 2>/dev/null | wc -l)
if [ "$DOC_FILES" -ge 3 ]; then
  SCORE=$((SCORE + 10))
  echo "  ✅ Documentation: 10/10"
else
  echo "  ⚠️ Documentation: $((DOC_FILES * 3))/10"
  SCORE=$((SCORE + DOC_FILES * 3))
fi

# Security (10 points)
if grep -q "rate_limit\|security" middleware/*.py 2>/dev/null; then
  SCORE=$((SCORE + 10))
  echo "  ✅ Security: 10/10"
else
  echo "  ⚠️ Security: 5/10"
  SCORE=$((SCORE + 5))
fi

# AI/ML (10 points)
if [ -d "services/agents" ] && [ -f "services/rag_service.py" ]; then
  SCORE=$((SCORE + 10))
  echo "  ✅ AI/ML: 10/10"
else
  echo "  ⚠️ AI/ML: 5/10"
  SCORE=$((SCORE + 5))
fi

echo ""
echo "─────────────────────────────────────────────────────────"
echo "  TOTAL SCORE: $SCORE/$MAX"
echo "─────────────────────────────────────────────────────────"
echo ""

if [ "$SCORE" -ge 90 ]; then
  echo "  🎉 EXCELLENT - Production Ready!"
elif [ "$SCORE" -ge 75 ]; then
  echo "  ✅ GOOD - Ready with minor improvements"
elif [ "$SCORE" -ge 60 ]; then
  echo "  ⚠️ FAIR - Needs work before production"
else
  echo "  ❌ POOR - Not ready for production"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ AUDIT COMPLETE - $(date)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
