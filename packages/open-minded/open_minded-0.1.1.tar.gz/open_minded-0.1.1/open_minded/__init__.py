from contextlib import asynccontextmanager
import logging

from open_minded.models.llm_message import LlmMessage
from open_minded.providers import get_provider_classes_shuffled
from open_minded.utils.errors import FailedToFindSuitableProviderError, OpenMindedError
from open_minded.utils.logging import setup_logging


setup_logging()
_logger = logging.getLogger("open_minded")


async def fetch_llm_completion(message_history: list[LlmMessage]):
    shuffled_providers = get_provider_classes_shuffled()

    for provider_class in shuffled_providers:
        try:
            async with provider_class() as provider:
                return {
                    "provider": provider,
                    "result": await provider.fetch_llm_completion(message_history),
                }
        except OpenMindedError as error:
            _logger.warning(
                f"Failed to fetch completion from {provider_class.name}: {error}.\nTrying other providers..."
            )

    raise FailedToFindSuitableProviderError()


@asynccontextmanager
async def fetch_llm_completion_and_stream(message_history: list[LlmMessage]):
    shuffled_providers = get_provider_classes_shuffled()

    for provider_class in shuffled_providers:
        try:
            async with (
                provider_class() as provider,
                provider.fetch_llm_completion_and_stream(message_history) as response,
            ):
                yield {
                    "provider": provider,
                    "result": response,
                }
                return
        except Exception as error:
            _logger.warning(
                f"Failed to fetch completion from {provider_class}: {error}.\nTrying other providers..."
            )

    raise FailedToFindSuitableProviderError()
