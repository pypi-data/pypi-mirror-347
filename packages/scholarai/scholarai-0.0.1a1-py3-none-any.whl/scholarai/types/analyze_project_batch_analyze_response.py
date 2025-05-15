# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["AnalyzeProjectBatchAnalyzeResponse"]


class AnalyzeProjectBatchAnalyzeResponse(BaseModel):
    response: Optional[str] = None
    """A markdown string that must be repeated verbatim.

    NEVER summarize any part of the response, ALWAYS repeat it directly
    """

    tool_hint: Optional[str] = None
    """A hint you MUST follow with regards to this response"""
