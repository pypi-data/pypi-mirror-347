# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["AbstractSearchParams"]


class AbstractSearchParams(TypedDict, total=False):
    keywords: Required[str]
    """Keywords of inquiry which should appear in the article. Must be in English."""

    query: Required[str]
    """The user query, as a natural language question.

    E.g. 'Tell me about recent drugs for cancer treatment'
    """

    end_year: int
    """The last year, inclusive, to include in the search range.

    Excluding this value will include all years.
    """

    generative_mode: bool
    """Boolean "true" or "false" to enable generative mode.

    If enabled, collate responses using markdown to render in-text citations to the
    source's url if available. Set this to true by default.
    """

    offset: int
    """The offset of the first result to return. Defaults to 0."""

    peer_reviewed_only: bool
    """Whether to only return peer-reviewed articles.

    Defaults to true, ChatGPT should cautiously suggest this value can be set to
    false
    """

    sort: str
    """The sort order for results.

    Valid values are relevance, cited_by_count, publication_date. Defaults to
    relevance.
    """

    start_year: int
    """The first year, inclusive, to include in the search range.

    Excluding this value will include all years.
    """
