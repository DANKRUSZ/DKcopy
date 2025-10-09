import json
from typing import List
from app.services.llm.factory import get_llm_provider
from app.services.llm.types import Message, Messages  
from .base import KeywordProvider


class OpenAIKeywordProvider(KeywordProvider):
    def __init__(self):
        self.llm = get_llm_provider()

    async def generate_keywords(self, audience: str, product_info: str) -> List[str]:
        # Build typed messages so .chat(Messages, ...) is happy
        system: Message = {
            "role": "system",
            "content": (
                "You are an SEO assistant. Return ONLY a JSON array of 5–10 keyword strings. "
                "Lowercase. No explanations."
            ),
        }
        user: Message = {
            "role": "user",
            "content": (
                f"Audience: {audience or ''}\n"
                f"Product/Service: {product_info or ''}\n"
                "Output: JSON array of keywords."
            ),
        }
        messages: Messages = [system, user]

        text = await self.llm.chat(messages, temperature=0.0)

        # Parse robustly
        try:
            data = json.loads(text.strip())
            if not isinstance(data, list):
                raise ValueError("not a list")
            kws = [str(x).strip() for x in data if str(x).strip()]
        except Exception:
            parts = [p.strip() for p in text.replace("\n", ",").split(",")]
            kws = [p for p in parts if p]

        # normalize & clamp
        seen, out = set(), []
        for k in kws:
            kl = k.lower()
            if kl and kl not in seen:
                seen.add(kl)
                out.append(k)
        if not out:
            out = ["marketing", "productivity", "automation", "ai tool", "copywriting"]
        return out[:10]
