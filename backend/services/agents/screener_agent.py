from typing import Dict, Any
from .base_agent import BaseAgent

class ScreenerAgent(BaseAgent):
    """Agent filtrujący - sprawdza must-have requirements"""
    
    def __init__(self):
        super().__init__(
            name="ScreenerAgent",
            description="Filters candidates by must-have skills"
        )
    
    async def process(self, cv_data: Dict[str, Any], job_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Sprawdza czy kandydat spełnia MUST-HAVE requirements"""
        
        cv_skills = set(str(s).lower() for s in cv_data.get('skills', []))
        must_have = set(str(s).lower() for s in job_requirements.get('must_have', []))
        
        missing_skills = must_have - cv_skills
        matching_skills = must_have & cv_skills
        
        passes = len(missing_skills) == 0
        match_percentage = (len(matching_skills) / len(must_have) * 100) if must_have else 100
        
        return {
            "passes": passes,
            "matching_skills": list(matching_skills),
            "missing_skills": list(missing_skills),
            "match_percentage": match_percentage,
            "confidence": "high" if match_percentage >= 80 else "medium" if match_percentage >= 50 else "low"
        }
