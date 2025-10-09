import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_llm(monkeypatch):
    """Mock the LLM to avoid API calls in tests"""
    from app import llm
    
    async def fake_keywords(self, audience, product_info):
        return ["test", "keyword", "mock"]
    
    async def fake_copy(self, request, keywords):
        if request.cta:
            return "Great copy here. CTA: Click now!"
        return "Great copy here."
    
    monkeypatch.setattr(llm.CopywritingLLM, "generate_keywords", fake_keywords)
    monkeypatch.setattr(llm.CopywritingLLM, "generate_copy", fake_copy)
