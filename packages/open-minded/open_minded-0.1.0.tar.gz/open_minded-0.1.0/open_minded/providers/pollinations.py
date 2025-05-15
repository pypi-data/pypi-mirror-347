from contextlib import asynccontextmanager
import json

import httpx

from open_minded.providers.base import LlmApiProvider
from open_minded.models.llm_message import LlmMessage
from open_minded.utils.errors import LlmApiHttpStatusError


_API_BASE_URL = "https://text.pollinations.ai"


class PollinationsProvider(LlmApiProvider):
    async def __aenter__(self):
        self.httpx_client = httpx.AsyncClient(base_url=_API_BASE_URL)
        return self

    async def __aexit__(self, *args):
        await self.httpx_client.__aexit__(*args)

    @property
    def name(self):
        return "Pollinations (https://pollinations.ai/)"

    async def fetch_llm_completion(self, message_history):
        async with self.fetch_llm_completion_response(message_history) as response:
            return response.text

    @asynccontextmanager
    async def fetch_llm_completion_and_stream(self, message_history):
        async with self.fetch_llm_completion_response(message_history) as response:

            async def stream_response():
                buffer = ""
                async for chunk in response.aiter_text():
                    buffer += chunk
                    lines = buffer.split("\n")
                    buffer = lines.pop()  # Save incomplete JSON

                    for line in lines:
                        line = line.strip()
                        if line.startswith("data: "):
                            data = line.replace("data: ", "").strip()
                            if data == "[DONE]":
                                return

                            try:
                                parsed = json.loads(data)
                                content = (
                                    parsed.get("choices", [{}])[0]
                                    .get("delta", {})
                                    .get("content")
                                )
                                if content:
                                    yield content
                            except (json.JSONDecodeError, IndexError, AttributeError):
                                continue

            yield stream_response()

    @asynccontextmanager
    async def fetch_llm_completion_response(self, message_history: list[LlmMessage]):
        async with self.httpx_client.stream(
            method="POST",
            url="/openai",
            headers={
                "Content-Type": "application/json",
                "Accept": "text/event-stream",
            },
            json={
                "model": "openai",
                "messages": message_history,
                "private": True,
                "stream": True,
            },
        ) as response:
            if response.is_error:
                raise LlmApiHttpStatusError(
                    response.status_code,
                    f"Failed to fetch GPT completion from deepai.com: {response.text}",
                )

            yield response
