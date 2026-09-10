import asyncio
import logging
from typing import Any, Callable, Optional

import aiohttp

from models import StructuredAnswer


LOGGER = logging.getLogger(__name__)


class LLMError(Exception):
    """Base exception for LLM client failures."""


class LLMTimeoutError(LLMError):
    """Raised when the LLM request exceeds its timeout."""


class LLMRequestError(LLMError):
    """Raised for transport, HTTP, or malformed provider response errors."""

# 主类
class LLMClient:
    # 构造函数
    def __init__(
        self,
        *,
        api_url: str,
        api_key: str,
        model: str,
        timeout_seconds: float = 30.0,
        session_factory: Optional[Callable[[], Any]] = None, # Optional选择参数可空，Callable[[],Any]:参数队列为空的方法，返回值为任意
    ) -> None:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero")

        self.api_url = api_url
        self.api_key = api_key
        self.model = model
        self.timeout_seconds = timeout_seconds
        self._session_factory = session_factory
        self._session: Optional[Any] = None
        self._owns_session = session_factory is None #session工厂：连接池

    async def __aenter__(self) -> "LLMClient":
        self._get_session()
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        await self.close()

    async def close(self) -> None:
        if (
            self._owns_session
            and self._session is not None
            and not getattr(self._session, "closed", False)
        ):
            await self._session.close()
            # await asyncio.sleep(0.25)

    async def request(self, prompt: str) -> StructuredAnswer:
        """Send one prompt and validate the assistant JSON response."""
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Return only JSON with a non-empty 'answer' string and an "
                        "optional 'confidence' number from 0 to 1."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        }
        headers = {
            "Authorization": "Bearer {0}".format(self.api_key),
            "Content-Type": "application/json",
        }

        LOGGER.info("LLM request started: model=%s endpoint=%s", self.model, self.api_url)
        try:
            session = self._get_session()
            async with session.post(self.api_url, headers=headers, json=payload) as response:
                if not 200 <= response.status < 300:
                    body = await response.text()
                    raise LLMRequestError(
                        "LLM request failed with HTTP {0}: {1}".format(
                            response.status, body[:200]
                        )
                    )

                response_payload = await response.json()
                LOGGER.info(response_payload)
        except asyncio.TimeoutError as error:
            LOGGER.warning("LLM request timed out after %s seconds", self.timeout_seconds)
            raise LLMTimeoutError(
                "LLM request timed out after {0} seconds".format(self.timeout_seconds)
            ) from error
        except aiohttp.ClientError as error:
            LOGGER.warning("LLM request failed: %s", error)
            raise LLMRequestError("LLM network request failed: {0}".format(error)) from error

        try:
            content = response_payload["choices"][0]["message"]["content"]
        except (IndexError, KeyError, TypeError) as error:
            raise LLMRequestError("LLM response did not contain assistant content") from error

        if not isinstance(content, str):
            raise LLMRequestError("LLM assistant content must be a JSON string")

        result = StructuredAnswer.model_validate_json(content)
        LOGGER.info("LLM request completed: model=%s", self.model)
        return result

    def _get_session(self) -> Any:
        if self._session is None:
            if self._session_factory is not None:
                self._session = self._session_factory()
            else:
                timeout = aiohttp.ClientTimeout(total=self.timeout_seconds)
                self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session
