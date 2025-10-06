from abc import ABC, abstractmethod
from typing import List

class KeywordProvider(ABC):
    @abstractmethod
    async def generate_keywords(self, audience: str, product_info: str) -> List[str]:
        ...
