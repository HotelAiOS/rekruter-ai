import pytest
from config import settings, get_settings

def test_settings_singleton():
    """Test that get_settings returns same instance"""
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2

def test_environment_properties():
    """Test environment detection properties"""
    if settings.ENVIRONMENT == "development":
        assert settings.is_development is True
        assert settings.is_production is False
    elif settings.ENVIRONMENT == "production":
        assert settings.is_development is False
        assert settings.is_production is True

def test_redis_available_property():
    """Test redis availability check"""
    if settings.REDIS_ENABLED and settings.REDIS_URL:
        assert settings.redis_available is True
    else:
        assert settings.redis_available is False

def test_default_values():
    """Test that critical settings have defaults"""
    assert settings.OLLAMA_BASE_URL is not None
    assert settings.OLLAMA_MODEL is not None
    assert settings.SECRET_KEY is not None
    assert settings.API_VERSION is not None

def test_feature_flags():
    """Test that feature flags are boolean"""
    assert isinstance(settings.USE_MULTI_AGENT, bool)
    assert isinstance(settings.USE_RAG_CONTEXT, bool)
    assert isinstance(settings.USE_KAIZEN_LEARNING, bool)
    assert isinstance(settings.ENABLE_FALLBACK, bool)
