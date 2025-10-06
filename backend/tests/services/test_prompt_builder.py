# tests/services/test_prompt_builder.py
from app.schemas.copy import CopyRequest
from app.services.prompt_builder import build_prompt

def test_prompt_returns_chat_messages():
    req = CopyRequest(
        content_type="Landing page hero",
        audience="freelancers",
        product_info="AI proposal tool",
        cta=True,
        tone_of_voice="friendly, confident"
    )
    messages = build_prompt(req)
    assert isinstance(messages, list)
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert "Landing page hero" in messages[1]["content"]
    assert "End with one clear call-to-action." in messages[1]["content"]

def test_prompt_no_cta_guardrail():
    req = CopyRequest(
        content_type="Facebook ad",
        audience="marketers",
        product_info="CRM tool",
        cta=False
    )
    messages = build_prompt(req)
    assert "Do not include a call-to-action." in messages[1]["content"]
