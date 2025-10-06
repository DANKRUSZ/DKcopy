from app.services.llm.factory import get_llm_provider
from app.services.llm.types import Messages

MAX_ALLOWED_LEN = 2000  # example guardrail

class CopyGenerator:
    def __init__(self):
        self.llm = get_llm_provider()

    async def generate(self, messages: Messages, temperature: float, require_cta: bool) -> str:
        text = await self.llm.chat(messages, temperature)

        if len(text) > MAX_ALLOWED_LEN:
            raise ValueError("Model output too long")

        if require_cta and "CTA:" not in text:
            raise ValueError("CTA missing from output")

        return text
