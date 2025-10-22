from abc import ABC
from typing import Any, Dict
from datetime import datetime

class BaseAgent:
    """Base class dla wszystkich specialized agents"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.memory = []
    
    # Removed @abstractmethod - each agent can have its own signature
    async def process(self, *args, **kwargs) -> Dict[str, Any]:
        """Główna logika agenta - implemented by subclasses"""
        raise NotImplementedError(f"{self.name} must implement process()")
    
    def log_interaction(self, input_data: Dict, output: Dict):
        """Log dla Kaizen learning"""
        self.memory.append({
            "input": input_data,
            "output": output,
            "timestamp": datetime.now()
        })
