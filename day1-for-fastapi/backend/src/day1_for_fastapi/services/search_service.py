import asyncio
from typing import Any

from ddgs import DDGS
from ddgs.exceptions import DDGSException

from .models import SearchResponse, SearchResult


class SearchError(Exception):
    """Raised when the search provider fails."""


def _search_text(query: str, max_results: int) -> list[dict[str, Any]]:
    with DDGS(timeout=10) as ddgs:
        return ddgs.text(
            query,
            region="cn-zh",
            safesearch="moderate",
            max_results=max_results,
        )


async def search(message: str, max_results: int = 5) -> SearchResponse:
    query = message.strip()
    if not query:
        raise ValueError("message is required")

    try:
        raw_results = await asyncio.to_thread(_search_text, query, max_results)
    except DDGSException as error:
        raise SearchError("search request failed") from error

    results = [
        SearchResult(
            title=str(item.get("title") or ""),
            href=str(item.get("href") or ""),
            body=str(item.get("body") or ""),
        )
        for item in raw_results
    ]
    return SearchResponse(query=query, results=results)
