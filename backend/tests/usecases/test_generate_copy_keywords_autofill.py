import pytest
from app.usecases.generate_copy import CopyGenerator
from app.schemas.copy import CopyRequest

@pytest.mark.asyncio
async def test_autofill_keywords_and_echo(monkeypatch):
    gen = CopyGenerator()

    async def fake_chat(messages, temperature):
        return "Some persuasive copy. CTA: Try it today."
    monkeypatch.setattr(gen.llm, "chat", fake_chat)

    req = CopyRequest(
        content_type="Landing page hero",
        audience="busy freelancers",
        product_info="An AI tool that drafts client proposals",
        cta=True,
        keywords=None,  # force the pre-step
    )

    text, final_keywords = await gen.generate(req, temperature=0.2, require_cta=True)

    assert "CTA" in text
    assert isinstance(final_keywords, list) and len(final_keywords) >= 5
