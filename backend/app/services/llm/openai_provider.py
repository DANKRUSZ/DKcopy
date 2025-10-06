from .base import LLMProvider
from .types import Messages
from app.core.config import settings
from openai import AsyncOpenAI

def _supports_temperature(model: str) -> bool:
    """
    GPT-5 family ignores/deprecates temperature for chat responses.
    Keep temperature for older models or other providers.
    """
    m = model.lower()
    if m.startswith("gpt-5"):
        return False
    # adjust as needed if you add non-OpenAI models
    return True

class OpenAIProvider(LLMProvider):
    def __init__(self):
        self._client = AsyncOpenAI(api_key=settings.OPEN_API_KEY)
        self._model = settings.OPENAI_MODEL  # e.g. "gpt-5"

    async def chat(self, messages: Messages, temperature: float = 0.2) -> str:
        kwargs = {
            "model": self._model,
            "messages": messages,
        }
        if _supports_temperature(self._model):
            kwargs["temperature"] = temperature

        # Use chat.completions for simplicity; swap to responses API if desired.
        resp = await self._client.chat.completions.create(**kwargs)
        return resp.choices[0].message.content or ""
