from app.core.config import settings
from .fake import FakeKeywordProvider

def get_keyword_provider():
    prov = (getattr(settings, "KEYWORD_PROVIDER", "fake") or "fake").lower()
    if prov == "openai":
        from .openai_provider import OpenAIKeywordProvider
        return OpenAIKeywordProvider()
    return FakeKeywordProvider()
