import pytest
from app.llm import FakeCopywritingLLM
from app.schemas import CopyRequest

@pytest.mark.asyncio
async def test_fake_llm_generates_keywords():
    llm = FakeCopywritingLLM()
    keywords = await llm.generate_keywords("freelancers", "AI tool")
    assert isinstance(keywords, list)
    assert len(keywords) > 0

@pytest.mark.asyncio
async def test_fake_llm_generates_copy_with_cta():
    llm = FakeCopywritingLLM()
    req = CopyRequest(
        content_type="Landing page",
        audience="developers",
        product_info="Code editor",
        cta=True
    )
    copy = await llm.generate_copy(req, ["test"])
    assert "CTA" in copy

@pytest.mark.asyncio
async def test_fake_llm_too_long_mode():
    llm = FakeCopywritingLLM(mode="too_long")
    req = CopyRequest(
        content_type="Ad",
        audience="users",
        product_info="Product",
        cta=False
    )
    copy = await llm.generate_copy(req, [])
    assert len(copy) > 2000