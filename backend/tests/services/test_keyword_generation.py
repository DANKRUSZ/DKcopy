import pytest
from app.services.llm.keywords.fake import FakeKeywordProvider

@pytest.mark.asyncio
async def test_fake_keyword_generation_returns_list():
    kp = FakeKeywordProvider()
    kws = await kp.generate_keywords("freelancers", "AI copywriting tool")
    assert isinstance(kws, list)
    assert 5 <= len(kws) <= 10
    assert all(isinstance(k, str) and k for k in kws)
