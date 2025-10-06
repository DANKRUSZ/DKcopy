from abc import ABC, abstractmethod
from .types import Messages

class LLMProvider(ABC):
    @abstractmethod
    async def chat(self, messages: Messages, temperature: float = 0.2) -> str:
        ...
