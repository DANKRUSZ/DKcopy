import pytest
from app.services.llm.fake_provider import FakeProvider
from app.usecases.generate_copy import CopyGenerator
from app.services.llm.types import Messages

@pytest.mark.anyio
async def test_fake_compliant_passes():
    gen = CopyGenerator()
    gen.llm = FakeProvider(mode="compliant")
    messages: Messages = [
        {"role": "system", "content": "You are an expert DR copywriter."},
        {"role": "user", "content": "Write a landing page hero. include CTA."},
    ]
    out = await gen.generate(messages, temperature=0.0, require_cta=True)
    assert "CTA:" in out

@pytest.mark.anyio
async def test_fake_too_long_fails():
    gen = CopyGenerator()
    gen.llm = FakeProvider(mode="too_long")
    with pytest.raises(ValueError, match="too long"):
        await gen.generate([], temperature=0.0, require_cta=False)

@pytest.mark.anyio
async def test_fake_missing_cta_fails():
    gen = CopyGenerator()
    gen.llm = FakeProvider(mode="missing_cta")
    with pytest.raises(ValueError, match="CTA missing"):
        await gen.generate([], temperature=0.0, require_cta=True)
