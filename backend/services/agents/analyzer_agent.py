from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from services.llm_service import LLMService

class AnalyzerAgent(BaseAgent):
    """Agent analizujący - głęboka analiza experience + skills"""
    
    def __init__(self):
        super().__init__(
            name="AnalyzerAgent",
            description="Deep analysis of experience and qualifications"
        )
        self.llm = LLMService()
    
    async def process(self, cv_data: Dict[str, Any], job_requirements: Dict[str, Any], context: Optional[str] = None) -> Dict[str, Any]:
        """
        Głęboka analiza kandydata
        Input: cv_data, job_requirements, context (optional)
        Output: strengths, weaknesses, red_flags, opportunities
        """
        
        experience = cv_data.get('experience', [])
        education = cv_data.get('education', [])
        skills = cv_data.get('skills', [])
        
        # Build prompt with optional context
        prompt = ""
        if context:
            prompt += f"COMPANY CONTEXT:\n{context}\n\n"
        
        prompt += f"""You are a SENIOR recruitment analyst with 15+ years experience.

CANDIDATE PROFILE:
- Skills: {skills}
- Experience: {experience}
- Education: {education}

JOB REQUIREMENTS:
Must have: {job_requirements.get('must_have', [])}
Nice to have: {job_requirements.get('nice_to_have', [])}

Task: Perform DEEP analysis. Look beyond keywords - analyze:
1. Years of relevant experience
2. Career progression
3. Technology stack evolution
4. Education relevance
5. Potential red flags (job hopping, skill gaps, etc.)

Return ONLY valid JSON:
{{
    "strengths": ["strength1", "strength2", "strength3"],
    "weaknesses": ["weakness1", "weakness2"],
    "red_flags": ["flag1", "flag2"] or [],
    "opportunities": ["opportunity1"],
    "seniority_level": "junior/mid/senior/lead",
    "culture_fit_notes": "brief notes",
    "detailed_reasoning": "2-3 sentences explaining your analysis"
}}

Be thorough but concise.
"""
        
        response = await self.llm.generate(prompt, system="You are a senior recruitment analyst. Return only JSON.")
        
        try:
            result = self.llm.extract_json(response)
            return result
            
        except Exception as e:
            print(f"❌ AnalyzerAgent Error: {e}")
            return {
                "strengths": [],
                "weaknesses": ["Analysis failed"],
                "red_flags": [],
                "opportunities": [],
                "seniority_level": "unknown",
                "culture_fit_notes": "N/A",
                "detailed_reasoning": "Error in analysis"
            }
