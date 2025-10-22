import logging

logger = logging.getLogger(__name__)

from typing import Dict, Any
from .screener_agent import ScreenerAgent
from .analyzer_agent import AnalyzerAgent
from .scorer_agent import ScorerAgent
from config import settings

class MultiAgentOrchestrator:
    """Orchestrates multiple AI agents for candidate evaluation"""
    
    def __init__(self):
        self.screener = ScreenerAgent()
        self.analyzer = AnalyzerAgent()
        self.scorer = ScorerAgent()
        
        logger.info("🤖 Multi-Agent System initialized")
        logger.info("   - ScreenerAgent: Filters candidates by must-have skills")
        logger.info("   - AnalyzerAgent: Deep analysis of experience and qualifications")
        logger.info("   - ScorerAgent: Final scoring and recommendation")
        
        if settings.USE_RAG_CONTEXT:
            logger.info("   - RAG Context: ✅ ENABLED")
    
    async def process_candidate(
        self, 
        cv_data: Dict[str, Any], 
        job_requirements: Dict[str, Any],
        company_id: str = None
    ) -> Dict[str, Any]:
        """Process candidate through multi-agent pipeline"""
        
        logger.info("\n🚀 Starting Multi-Agent Pipeline...")
        
        # Get RAG context if enabled
        company_context = ""
        if settings.USE_RAG_CONTEXT:
            try:
                from services.rag_service import get_rag
                rag = get_rag()
                if rag:
                    query = f"Hiring for {job_requirements.get('title', 'position')} with skills {job_requirements.get('must_have', [])}"
                    company_context = rag.build_context(query, company_id=company_id)
                    logger.info(f"   📚 RAG Context loaded: {len(company_context)} chars")
            except Exception as e:
                logger.info(f"   ⚠️ RAG Context failed: {e}")
        
        # Stage 1: Screener
        logger.info("   1️⃣ ScreenerAgent checking requirements...")
        screening_result = await self.screener.process(cv_data, job_requirements)
        logger.info(f"      ✅ Passes screening: {screening_result.get('passes', False)}")
        
        # Stage 2: Analyzer (with RAG context)
        logger.info("   2️⃣ AnalyzerAgent performing deep analysis...")
        analysis_result = await self.analyzer.process(
            cv_data, 
            job_requirements,
            context=company_context if company_context else None
        )
        logger.info(f"      ✅ Strengths found: {len(analysis_result.get('strengths', []))}")
        
        # Stage 3: Scorer
        logger.info("   3️⃣ ScorerAgent calculating final score...")
        scoring_result = await self.scorer.process(
            cv_data,
            job_requirements,
            screening_result,
            analysis_result
        )
        logger.info(f"      ✅ Final score: {scoring_result.get('score', 0)}/100")
        logger.info(f"      ✅ Recommendation: {scoring_result.get('recommendation', 'unknown')}")
        
        logger.info("\n✨ Multi-Agent Pipeline completed!")
        
        return scoring_result

    def log_decision_to_kaizen(self, candidate_id: str, result: Dict):
        """Log decision to Kaizen for learning"""
        from config import settings
        if settings.USE_KAIZEN_LEARNING:
            try:
                from services.kaizen_engine import kaizen_engine
                kaizen_engine.log_decision(
                    candidate_id=candidate_id,
                    decision=result.get("recommendation", "unknown"),
                    reasoning=result.get("reasoning", "")
                )
            except Exception as e:
                logger.info(f"⚠️ Kaizen logging failed: {e}")
