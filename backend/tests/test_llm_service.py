import pytest
from services.llm_service import LLMService
import json

class TestLLMService:
    """Test LLM Service functionality"""
    
    @pytest.fixture
    def llm_service(self):
        return LLMService()
    
    def test_extract_json_from_dict(self, llm_service):
        """Test extracting JSON when already a dict"""
        test_dict = {"name": "John", "age": 30}
        result = llm_service.extract_json(test_dict)
        
        assert result == test_dict
    
    def test_extract_json_from_string(self, llm_service):
        """Test extracting JSON from string"""
        test_str = '{"name": "John", "age": 30}'
        result = llm_service.extract_json(test_str)
        
        assert isinstance(result, dict)
        assert result["name"] == "John"
    
    def test_extract_json_from_markdown(self, llm_service):
        """Test extracting JSON from markdown code block"""
        test_str = '``````'
        result = llm_service.extract_json(test_str)
        
        assert isinstance(result, dict) or isinstance(result, str)
    
    def test_extract_json_invalid(self, llm_service):
        """Test extracting JSON from invalid string"""
        test_str = "Not valid JSON at all"
        result = llm_service.extract_json(test_str)
        
        # Should return original string or empty dict
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_parse_cv_empty(self, llm_service):
        """Test parsing empty CV text"""
        result = await llm_service.parse_cv("")
        
        assert isinstance(result, dict)
    
    @pytest.mark.asyncio
    async def test_score_candidate_basic(self, llm_service):
        """Test basic candidate scoring"""
        cv_data = {
            "skills": ["Python", "FastAPI"],
            "name": "Test User"
        }
        job_requirements = {
            "must_have": ["Python", "FastAPI"],
            "nice_to_have": ["Docker"]
        }
        
        result = await llm_service.score_candidate(cv_data, job_requirements)
        
        assert isinstance(result, dict)
        assert "score" in result
        assert isinstance(result["score"], int)
