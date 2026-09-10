from typing import Optional

from pydantic import BaseModel, Field


class StructuredAnswer(BaseModel):
    """The JSON shape requested from the LLM."""

    answer: str = Field(min_length=1)
    confidence: Optional[float] = Field(default=None, ge=0, le=1)
