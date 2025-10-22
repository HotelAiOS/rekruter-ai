from datetime import datetime, timedelta
from typing import Dict, List, Optional
from database import get_db
from models import Candidate
from sqlalchemy.orm import Session

class KaizenEngine:
    """Simple Kaizen Learning - learns from hiring outcomes"""
    
    def __init__(self):
        self.learning_data = []
        print("🎓 Kaizen Learning Engine initialized")
    
    def log_decision(self, candidate_id: str, decision: str, reasoning: str):
        """Log a hiring decision"""
        entry = {
            "candidate_id": candidate_id,
            "decision": decision,  # hired, rejected, maybe
            "reasoning": reasoning,
            "timestamp": datetime.now()
        }
        self.learning_data.append(entry)
        print(f"📝 Logged decision: {decision} for candidate {candidate_id}")
    
    async def collect_feedback(self, candidate_id: str, feedback: Dict):
        """Collect feedback on hired candidate after 1-6 months"""
        feedback_entry = {
            "candidate_id": candidate_id,
            "performance_rating": feedback.get("performance_rating", 0),  # 1-10
            "retention_months": feedback.get("retention_months", 0),
            "culture_fit_actual": feedback.get("culture_fit", 0),  # 1-10
            "notes": feedback.get("notes", ""),
            "timestamp": datetime.now()
        }
        
        # Trigger learning
        await self.learn_from_feedback(candidate_id, feedback_entry)
        
        print(f"✅ Feedback collected for {candidate_id}")
        return feedback_entry
    
    async def learn_from_feedback(self, candidate_id: str, feedback: Dict):
        """Learn from actual hiring outcomes"""
        # Get original candidate data
        db = next(get_db())
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        
        if not candidate:
            print(f"⚠️ Candidate {candidate_id} not found")
            return
        
        predicted_score = candidate.score
        actual_performance = feedback["performance_rating"] * 10  # Scale to 100
        
        # Calculate prediction error
        error = abs(predicted_score - actual_performance)
        
        if error > 20:
            print(f"⚠️ Large prediction error: {error} points!")
            print(f"   Predicted: {predicted_score}, Actual: {actual_performance}")
            
            # Log for review
            self.log_misprediction(candidate, feedback, error)
        else:
            print(f"✅ Good prediction! Error: {error} points")
    
    def log_misprediction(self, candidate, feedback, error):
        """Log cases where we were significantly wrong"""
        analysis = {
            "candidate_id": candidate.id,
            "predicted_score": candidate.score,
            "actual_performance": feedback["performance_rating"] * 10,
            "error": error,
            "profile": candidate.parsed_data,
            "original_analysis": candidate.analysis,
            "feedback": feedback,
            "timestamp": datetime.now()
        }
        
        # In future: use this to retrain models
        print(f"📊 Misprediction logged for analysis")
    
    def get_learning_stats(self) -> Dict:
        """Get learning statistics"""
        if not self.learning_data:
            return {"total_decisions": 0}
        
        return {
            "total_decisions": len(self.learning_data),
            "last_decision": self.learning_data[-1]["timestamp"],
            "decision_breakdown": self._count_decisions()
        }
    
    def _count_decisions(self) -> Dict:
        """Count decisions by type"""
        counts = {"hired": 0, "rejected": 0, "maybe": 0}
        for entry in self.learning_data:
            decision = entry["decision"]
            if decision in counts:
                counts[decision] += 1
        return counts

# Global instance
kaizen_engine = KaizenEngine()
