import logging

logger = logging.getLogger(__name__)

from typing import Dict, Any
from .base_agent import BaseAgent
from services.llm_service import LLMService

class ScorerAgent(BaseAgent):
    """Agent scoringowy - finalna ocena i rekomendacja"""
    
    def __init__(self):
        super().__init__(
            name="ScorerAgent",
            description="Final scoring and recommendation"
        )
        self.llm = LLMService()
    
    async def process(
        self, 
        cv_data: Dict[str, Any], 
        job_requirements: Dict[str, Any],
        screening_result: Dict[str, Any],
        analysis_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Finalna ocena i rekomendacja
        Input: cv_data, job_requirements, screening_result, analysis_result
        Output: score, recommendation, reasoning
        """
        
        # Get data from previous stages
        passes_screening = screening_result.get('passes', False)
        match_percentage = screening_result.get('match_percentage', 0)
        strengths = analysis_result.get('strengths', [])
        weaknesses = analysis_result.get('weaknesses', [])
        red_flags = analysis_result.get('red_flags', [])
        
        # Calculate base score
        base_score = match_percentage
        
        # Adjust score based on analysis
        score = base_score
        score += min(len(strengths) * 5, 20)  # Max +20 for strengths
        score -= min(len(weaknesses) * 3, 15)  # Max -15 for weaknesses
        score -= min(len(red_flags) * 10, 30)  # Max -30 for red flags
        
        # Ensure score is in range
        score = max(0, min(100, int(score)))
        
        # Determine recommendation
        if score >= 80:
            recommendation = "strong_yes"
            confidence = "high"
        elif score >= 60:
            recommendation = "yes"
            confidence = "medium"
        elif score >= 40:
            recommendation = "maybe"
            confidence = "medium"
        else:
            recommendation = "no"
            confidence = "high"
        
        # Build reasoning
        reasoning = f"Score {score}/100. Skills match: {match_percentage:.0f}%. "
        reasoning += f"{len(strengths)} strengths, {len(weaknesses)} weaknesses"
        if red_flags:
            reasoning += f", {len(red_flags)} red flags"
        reasoning += f". Recommendation: {recommendation}."
        
        return {
            "score": score,
            "recommendation": recommendation,
            "confidence": confidence,
            "strengths": strengths[:3],  # Top 3
            "weaknesses": weaknesses,
            "reasoning": reasoning
        }
