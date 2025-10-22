import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def test_cv_data():
    return {
        "name": "Jan Kowalski",
        "email": "jan@example.com",
        "skills": ["Python", "FastAPI", "PostgreSQL"],
        "experience": [{"company": "Tech Corp", "role": "Senior Developer", "duration": "2020-2023"}],
        "education": [{"degree": "MSc CS", "university": "AGH", "year": "2020"}]
    }
