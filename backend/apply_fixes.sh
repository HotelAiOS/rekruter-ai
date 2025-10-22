#!/bin/bash
echo "🔧 Applying fixes..."

# Fix 1: Update Pydantic schemas
echo "Fix 1: Pydantic ConfigDict..."
sed -i 's/class Config:/model_config = ConfigDict(from_attributes=True)\n    # Old Config:/g' schemas.py
echo "✅ Pydantic updated"

# Fix 2: Fix datetime.utcnow()
echo "Fix 2: datetime deprecations..."
sed -i 's/datetime.utcnow()/datetime.now(timezone.utc)/g' services/auth.py
sed -i '1 i\from datetime import timezone' services/auth.py
echo "✅ datetime updated"

# Fix 3: Add auth to failing tests
echo "Fix 3: Update tests with auth..."
cat >> tests/test_api.py << 'TESTFIX'

@pytest.mark.asyncio
async def test_create_job_with_auth(client: AsyncClient):
    # Login first
    login_resp = await client.post("/auth/login", data={
        "username": "user@app.io",
        "password": "test"
    })
    token = login_resp.json()["access_token"]
    
    # Create job with auth
    response = await client.post("/api/jobs", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Job",
            "description": "Test",
            "requirements": {"must_have": ["Python"], "nice_to_have": []}
        })
    assert response.status_code == 201
TESTFIX
echo "✅ Tests updated"

echo ""
echo "🎉 Fixes applied! Run tests again:"
echo "pytest tests/ -v --cov"
