import pytest
from database import get_db, check_db_connection
from config import settings

@pytest.mark.asyncio
async def test_check_db_connection():
    """Test database connection check"""
    result = await check_db_connection()
    assert "status" in result
    assert result["status"] in ["healthy", "unhealthy"]

@pytest.mark.asyncio
async def test_get_db_session():
    """Test database session creation"""
    async for session in get_db():
        assert session is not None
        break

def test_database_url_configured():
    """Test that DATABASE_URL is set"""
    assert settings.DATABASE_URL is not None
    assert len(settings.DATABASE_URL) > 0

def test_is_sqlite_property():
    """Test is_sqlite detection"""
    if "sqlite" in settings.DATABASE_URL.lower():
        assert settings.is_sqlite is True
    else:
        assert settings.is_sqlite is False
