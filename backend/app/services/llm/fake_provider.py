from .base import LLMProvider
from .types import Messages
from typing import Literal

FakeMode = Literal["compliant", "too_long", "missing_cta"]

COMPLIANT = (
    "Headline: Win Back Your Time\n\n"
    "Body: Freelancers love how this tool drafts proposals in minutes, "
    "in your voice, with zero hassle.\n\n"
    "CTA: Start your free trial today."
)

TOO_LONG = " ".join(["Long body"] * 800)

MISSING_CTA = (
    "Headline: Win Back Your Time\n\n"
    "Body: Freelancers love how this tool drafts proposals in minutes, "
    "in your voice, with zero hassle."
)

class FakeProvider(LLMProvider):
    def __init__(self, mode: FakeMode = "compliant"):
        self.mode = mode

    async def chat(self, messages: Messages, temperature: float = 0.0) -> str:
        if self.mode == "compliant":
            return COMPLIANT
        if self.mode == "too_long":
            return TOO_LONG
        if self.mode == "missing_cta":
            return MISSING_CTA
        return COMPLIANT
