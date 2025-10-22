import httpx
from typing import Dict, Any, Optional
from config import settings
import json
import re

class LLMService:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
    
    async def generate(self, prompt: str, system: Optional[str] = None) -> str:
        """Generate text using Ollama"""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        if system:
            payload["system"] = system
        
        try:
            async with httpx.AsyncClient(timeout=360.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return response.json().get("response", "")
        except Exception as e:
            print(f"❌ Ollama Error: {e}")
            return ""
    
    def extract_json(self, text: str) -> Any:
        """Extract JSON from text, handling both string and dict responses"""
        # If already a dict, return it
        if isinstance(text, dict):
            return text
        
        # Try to find JSON in markdown code blocks
        text = text.strip()
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except:
                pass
        
        # Try parsing whole text
        try:
            return json.loads(text)
        except:
            return text
    
    async def parse_cv(self, cv_text: str) -> Dict[str, Any]:
        """Parse CV text into structured data"""
        system_prompt = """You are a CV parser. Extract information and return ONLY valid JSON.
        Format: {"name":"...","email":"...","phone":"...","experience":[...],"skills":[...],"education":[],"languages":[]}"""
        
        user_prompt = f"Parse this CV and return ONLY JSON:\n\n{cv_text}"
        
        response = await self.generate(user_prompt, system=system_prompt)
        
        try:
            parsed = self.extract_json(response)
            print(f"✅ DEBUG PARSE_CV SUCCESS: {parsed.get('name', 'N/A')}")
            return parsed if isinstance(parsed, dict) else {}
        except Exception as e:
            print(f"❌ DEBUG PARSE_CV ERROR: {e}")
            print(f"📄 DEBUG PARSE_CV RAW (first 300): {str(response)[:300]}")
            return {}
    
    async def score_candidate(self, cv_data: Dict[str, Any], job_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Score candidate against job requirements"""
        system_prompt = """You are a recruiter. Score candidates 0-100.
        Return ONLY valid JSON: {"score":85,"strengths":[],"weaknesses":[],"recommendation":"yes/maybe/no","reasoning":"..."}"""
        
        skills = cv_data.get("skills", [])
        must_have = job_requirements.get("must_have", [])
        
        user_prompt = f"""Job requires: {must_have}
Candidate has: {skills}
Return ONLY JSON with score, strengths, weaknesses, recommendation, reasoning"""
        
        response = await self.generate(user_prompt, system=system_prompt)
        
        try:
            scored = self.extract_json(response)
            print(f"✅ DEBUG SCORE SUCCESS: score={scored.get('score')}")
            return scored if isinstance(scored, dict) else {"score": 0, "strengths": [], "weaknesses": ["Error"], "recommendation": "no", "reasoning": "Failed"}
        except Exception as e:
            print(f"❌ DEBUG SCORE ERROR: {e}")
            print(f"📄 DEBUG SCORE RAW (first 300): {str(response)[:300]}")
            return {"score": 0, "strengths": [], "weaknesses": ["Error"], "recommendation": "no", "reasoning": "Failed"}
