# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["PatentListParams"]


class PatentListParams(TypedDict, total=False):
    full_user_prompt: Required[str]
    """The entirety of the user request, directly quoted."""

    keywords: Required[str]
    """Keywords of inquiry which should appear in article. Must be in English."""

    query: Required[str]
    """The user query.

    If the user asks for a specific patent, you MUST hit the API using escaped
    quotation marks
    """

    end_year: str
    """The last year, inclusive, to include in the search range.

    Excluding this value will include all years.
    """

    generative_mode: str
    """Boolean "true" or "false" to enable generative mode.

    If enabled, collate responses using markdown to render in-text citations to the
    source's url if available. Set this to true by default.
    """

    offset: str
    """The offset of the first result to return. Defaults to 0."""

    peer_reviewed_only: str
    """Whether to only return peer reviewed articles.

    Defaults to true, ChatGPT should cautiously suggest this value can be set to
    false
    """

    sort: str
    """The sort order for results.

    Valid values are relevance, cited_by_count, publication_date. Defaults to
    relevance.
    """

    start_year: str
    """The first year, inclusive, to include in the search range.

    Excluding this value will include all years.
    """
