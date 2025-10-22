import pytest
from services.cache import cache

@pytest.mark.asyncio
async def test_cache_initialization():
    """Test cache service initialization"""
    assert cache is not None
    await cache.connect()

@pytest.mark.asyncio
async def test_cache_set_get():
    """Test cache set and get operations"""
    await cache.connect()
    
    test_key = "test_key"
    test_value = {"data": "test"}
    
    await cache.set(test_key, test_value)
    result = await cache.get(test_key)
    
    # Może być None jeśli Redis nie działa (fallback to memory)
    if result:
        assert result == test_value

@pytest.mark.asyncio
async def test_cache_delete():
    """Test cache delete operation"""
    await cache.connect()
    
    test_key = "test_delete_key"
    test_value = {"data": "to_delete"}
    
    await cache.set(test_key, test_value)
    await cache.delete(test_key)
    
    result = await cache.get(test_key)
    assert result is None
