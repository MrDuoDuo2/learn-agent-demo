import asyncio
import unittest
from typing import Any, Dict, Optional

import aiohttp
from pydantic import ValidationError

from llm_client import LLMClient, LLMRequestError, LLMTimeoutError


class FakeResponse:
    def __init__(
        self,
        *,
        status: int = 200,
        payload: Optional[Dict[str, Any]] = None,
        text: str = "",
        enter_error: Optional[BaseException] = None,
    ) -> None:
        self.status = status
        self._payload = payload or {}
        self._text = text
        self._enter_error = enter_error

    async def __aenter__(self) -> "FakeResponse":
        if self._enter_error is not None:
            raise self._enter_error
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        return None

    async def json(self) -> Dict[str, Any]:
        return self._payload

    async def text(self) -> str:
        return self._text


class FakeSession:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.requests = []
        self.closed = False

    def post(self, url: str, **kwargs: Any) -> FakeResponse:
        self.requests.append({"url": url, **kwargs})
        return self.response

    async def close(self) -> None:
        self.closed = True


class LLMClientTests(unittest.IsolatedAsyncioTestCase):
    async def test_request_parses_valid_assistant_json(self) -> None:
        """Removing the LLM content parsing must fail this test."""
        session = FakeSession(
            FakeResponse(
                payload={
                    "choices": [
                        {
                            "message": {
                                "content": '{"answer": "Paris", "confidence": 0.95}'
                            }
                        }
                    ]
                }
            )
        )
        client = LLMClient(
            api_url="https://example.test/v1/chat/completions",
            api_key="test-key",
            model="test-model",
            session_factory=lambda: session,
        )

        result = await client.request("What is the capital of France?")

        self.assertEqual(result.answer, "Paris")
        self.assertEqual(result.confidence, 0.95)
        self.assertEqual(session.requests[0]["json"]["model"], "test-model")
        self.assertEqual(
            session.requests[0]["json"]["messages"][1]["content"],
            "What is the capital of France?",
        )

    async def test_request_surfaces_invalid_structured_content(self) -> None:
        """Removing Pydantic output validation must fail this test."""
        session = FakeSession(
            FakeResponse(
                payload={
                    "choices": [
                        {"message": {"content": '{"answer": "Paris", "confidence": 2}'}}
                    ]
                }
            )
        )
        client = LLMClient(
            api_url="https://example.test/v1/chat/completions",
            api_key="test-key",
            model="test-model",
            session_factory=lambda: session,
        )

        with self.assertRaises(ValidationError):
            await client.request("What is the capital of France?")

    async def test_request_maps_timeout_to_client_error(self) -> None:
        """Removing timeout handling must fail this test."""
        session = FakeSession(FakeResponse(enter_error=asyncio.TimeoutError()))
        client = LLMClient(
            api_url="https://example.test/v1/chat/completions",
            api_key="test-key",
            model="test-model",
            session_factory=lambda: session,
        )

        with self.assertLogs("llm_client", level="WARNING"):
            with self.assertRaises(LLMTimeoutError):
                await client.request("Hello")

    async def test_request_maps_network_error_to_client_error(self) -> None:
        """Removing aiohttp error handling must fail this test."""
        session = FakeSession(
            FakeResponse(enter_error=aiohttp.ClientConnectionError("offline"))
        )
        client = LLMClient(
            api_url="https://example.test/v1/chat/completions",
            api_key="test-key",
            model="test-model",
            session_factory=lambda: session,
        )

        with self.assertLogs("llm_client", level="WARNING"):
            with self.assertRaises(LLMRequestError):
                await client.request("Hello")

    async def test_request_maps_http_error_to_client_error(self) -> None:
        """Removing HTTP status handling must fail this test."""
        session = FakeSession(FakeResponse(status=429, text="rate limit exceeded"))
        client = LLMClient(
            api_url="https://example.test/v1/chat/completions",
            api_key="test-key",
            model="test-model",
            session_factory=lambda: session,
        )

        with self.assertRaisesRegex(LLMRequestError, "HTTP 429"):
            await client.request("Hello")
