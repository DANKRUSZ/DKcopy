from copy import deepcopy
from typing import Any, Union  # <- remove List if present
from app.services.llm.factory import get_llm_provider
from app.services.llm.types import Messages
from app.services.prompt_builder import build_prompt
from app.schemas.copy import CopyRequest
from app.services.llm.keywords.fake import FakeKeywordProvider  # keep this if NOT using factory

MAX_ALLOWED_LEN = 2000

class CopyGenerator:
    def __init__(self):
        self.llm = get_llm_provider()
        self.keyword_provider = FakeKeywordProvider()  # keep if not using factory

    async def generate(
        self,
        req_or_messages: Union[CopyRequest, Messages],
        temperature: float,
        require_cta: bool,
    ) -> Any:
        if isinstance(req_or_messages, list):
            messages: Messages = req_or_messages
            text = await self.llm.chat(messages, temperature)
            if len(text) > MAX_ALLOWED_LEN:
                raise ValueError("Model output too long")
            if require_cta and "cta" not in text.lower():
                raise ValueError("CTA missing from output")
            return text

        req: CopyRequest = req_or_messages  # type: ignore[assignment]
        req2 = deepcopy(req)
        if not req2.keywords:
            req2.keywords = await self.keyword_provider.generate_keywords(
                audience=req2.audience or "",
                product_info=req2.product_info or "",
            )
        messages: Messages = build_prompt(req2)
        text = await self.llm.chat(messages, temperature)
        if len(text) > MAX_ALLOWED_LEN:
            raise ValueError("Model output too long")
        if require_cta and "cta" not in text.lower():
            raise ValueError("CTA missing from output")
        return text, req2.keywords
