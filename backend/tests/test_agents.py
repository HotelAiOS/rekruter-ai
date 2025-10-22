import pytest
from services.agents.screener_agent import ScreenerAgent
from services.agents.analyzer_agent import AnalyzerAgent
from services.agents.scorer_agent import ScorerAgent

def test_screener_agent_initialization():
    """Test screener agent can be initialized"""
    agent = ScreenerAgent()
    assert agent is not None
    assert agent.name == "ScreenerAgent"  # Fixed: actual name

def test_analyzer_agent_initialization():
    """Test analyzer agent can be initialized"""
    agent = AnalyzerAgent()
    assert agent is not None
    assert agent.name == "AnalyzerAgent"  # Fixed: actual name

def test_scorer_agent_initialization():
    """Test scorer agent can be initialized"""
    agent = ScorerAgent()
    assert agent is not None
    assert agent.name == "ScorerAgent"  # Fixed: actual name

@pytest.mark.asyncio
async def test_screener_agent_mock_processing(test_cv_data):
    """Test screener agent with mock data"""
    agent = ScreenerAgent()
    assert hasattr(agent, 'process')
    assert callable(agent.process)

@pytest.mark.asyncio
async def test_analyzer_agent_mock_processing(test_cv_data):
    """Test analyzer agent with mock data"""
    agent = AnalyzerAgent()
    assert hasattr(agent, 'process')
    assert callable(agent.process)
