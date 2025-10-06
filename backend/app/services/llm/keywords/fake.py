from typing import List
from .base import KeywordProvider

class FakeKeywordProvider(KeywordProvider):
    async def generate_keywords(self, audience: str, product_info: str) -> List[str]:
        # deterministic and short for tests
        return [
            "ai tool", "copywriting", "automation", "marketing",
            "freelancers", "productivity", "business growth"
        ]