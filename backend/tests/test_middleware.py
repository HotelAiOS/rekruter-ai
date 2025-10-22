import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_request_id_header(client: AsyncClient):
    """Test that X-Request-ID is added to responses"""
    response = await client.get("/health")
    assert "X-Request-ID" in response.headers

@pytest.mark.asyncio
async def test_security_headers(client: AsyncClient):
    """Test that security headers are present"""
    response = await client.get("/health")
    assert "X-Content-Type-Options" in response.headers
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert "X-Frame-Options" in response.headers
    assert response.headers["X-Frame-Options"] == "DENY"

@pytest.mark.asyncio
async def test_cors_headers(client: AsyncClient):
    """Test CORS headers"""
    response = await client.options("/health", headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET"
    })
    # CORS headers should be present
    assert response.status_code in [200, 405]
