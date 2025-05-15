# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["PaperMetadata"]


class PaperMetadata(BaseModel):
    abstract: Optional[str] = None
    """The abstract of this paper. Agentic endpoints may not have this entry."""

    answer: Optional[str] = None
    """Answer to the user query based on the information from this paper.

    Only available if generative_mode is set to true.
    """

    authors: Optional[List[str]] = None

    cited_by_count: Optional[int] = None

    doi: Optional[str] = None
    """Digital Object Identifier"""

    publication_date: Optional[str] = None

    ss_id: Optional[str] = None
    """Semantic Scholar ID"""

    title: Optional[str] = None

    url: Optional[str] = None
