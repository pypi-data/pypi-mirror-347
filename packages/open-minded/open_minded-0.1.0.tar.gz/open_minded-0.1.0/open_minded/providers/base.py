from abc import ABC, abstractmethod
from typing import AsyncContextManager

from open_minded.models.llm_message import LlmMessage


class LlmApiProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def fetch_llm_completion(self, message_history: list[LlmMessage]) -> str:
        pass

    @abstractmethod
    def fetch_llm_completion_and_stream(
        self, message_history: list[LlmMessage]
    ) -> AsyncContextManager:
        pass
