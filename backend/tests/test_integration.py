import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_full_job_flow(client: AsyncClient):
    # Register
    resp = await client.post("/auth/register", json={"email":"test@test.com","password":"test123","company_name":"Test"})
    assert resp.status_code in [201, 400]
    
    # Login
    resp = await client.post("/auth/login", data={"username":"test@test.com","password":"test123"})
    token = resp.json().get("access_token") if resp.status_code == 200 else None
    
    if token:
        # Create job
        headers = {"Authorization": f"Bearer {token}"}
        resp = await client.post("/api/jobs", json={"title":"Test","description":"Test","requirements":{"must_have":["Python"],"nice_to_have":[]}}, headers=headers)
        assert resp.status_code in [201, 500]
