from typing import Optional

from pydantic import BaseModel, Field


class StructuredAnswer(BaseModel):
    """The JSON shape requested from the LLM."""

    answer: str = Field(min_length=1)
    confidence: Optional[float] = Field(default=None, ge=0, le=1)


class SearchResult(BaseModel):
    """One text search result returned by DDGS."""

    title: str = ""
    href: str = ""
    body: str = ""


class SearchResponse(BaseModel):
    """The response shape returned by the /search endpoint."""

    query: str = Field(min_length=1)
    results: list[SearchResult] = Field(default_factory=list)
