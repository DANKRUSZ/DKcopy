from app.core.config import settings
from .base import LLMProvider
from .openai_provider import OpenAIProvider
from .fake_provider import FakeProvider, FakeMode

def get_llm_provider() -> LLMProvider:
    provider = settings.LLM_PROVIDER.lower()  # "openai" | "fake" | "fake:too_long" | "fake:missing_cta"
    if provider == "openai":
        return OpenAIProvider()
    if provider.startswith("fake"):
        _, *rest = provider.split(":")
        mode: FakeMode = (rest[0] if rest else "compliant")  # type: ignore
        return FakeProvider(mode=mode)  # type: ignore
    return FakeProvider(mode="compliant")
