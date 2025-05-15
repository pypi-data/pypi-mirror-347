# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import abstract_search_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.abstract_search_response import AbstractSearchResponse

__all__ = ["AbstractsResource", "AsyncAbstractsResource"]


class AbstractsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AbstractsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AbstractsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AbstractsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#with_streaming_response
        """
        return AbstractsResourceWithStreamingResponse(self)

    def search(
        self,
        *,
        keywords: str,
        query: str,
        end_year: int | NotGiven = NOT_GIVEN,
        generative_mode: bool | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        peer_reviewed_only: bool | NotGiven = NOT_GIVEN,
        sort: str | NotGiven = NOT_GIVEN,
        start_year: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AbstractSearchResponse:
        """Retrieves relevant abstracts and paper metadata by a search.

        Generates an answer
        using LLMs if generative_mode is set to true. For an API meant for faster and
        more replete data retrieval, use /api/fast_paper_search

        Args:
          keywords: Keywords of inquiry which should appear in the article. Must be in English.

          query: The user query, as a natural language question. E.g. 'Tell me about recent drugs
              for cancer treatment'

          end_year: The last year, inclusive, to include in the search range. Excluding this value
              will include all years.

          generative_mode: Boolean "true" or "false" to enable generative mode. If enabled, collate
              responses using markdown to render in-text citations to the source's url if
              available. Set this to true by default.

          offset: The offset of the first result to return. Defaults to 0.

          peer_reviewed_only: Whether to only return peer-reviewed articles. Defaults to true, ChatGPT should
              cautiously suggest this value can be set to false

          sort: The sort order for results. Valid values are relevance, cited_by_count,
              publication_date. Defaults to relevance.

          start_year: The first year, inclusive, to include in the search range. Excluding this value
              will include all years.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/abstracts",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "keywords": keywords,
                        "query": query,
                        "end_year": end_year,
                        "generative_mode": generative_mode,
                        "offset": offset,
                        "peer_reviewed_only": peer_reviewed_only,
                        "sort": sort,
                        "start_year": start_year,
                    },
                    abstract_search_params.AbstractSearchParams,
                ),
            ),
            cast_to=AbstractSearchResponse,
        )


class AsyncAbstractsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAbstractsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAbstractsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAbstractsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#with_streaming_response
        """
        return AsyncAbstractsResourceWithStreamingResponse(self)

    async def search(
        self,
        *,
        keywords: str,
        query: str,
        end_year: int | NotGiven = NOT_GIVEN,
        generative_mode: bool | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        peer_reviewed_only: bool | NotGiven = NOT_GIVEN,
        sort: str | NotGiven = NOT_GIVEN,
        start_year: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AbstractSearchResponse:
        """Retrieves relevant abstracts and paper metadata by a search.

        Generates an answer
        using LLMs if generative_mode is set to true. For an API meant for faster and
        more replete data retrieval, use /api/fast_paper_search

        Args:
          keywords: Keywords of inquiry which should appear in the article. Must be in English.

          query: The user query, as a natural language question. E.g. 'Tell me about recent drugs
              for cancer treatment'

          end_year: The last year, inclusive, to include in the search range. Excluding this value
              will include all years.

          generative_mode: Boolean "true" or "false" to enable generative mode. If enabled, collate
              responses using markdown to render in-text citations to the source's url if
              available. Set this to true by default.

          offset: The offset of the first result to return. Defaults to 0.

          peer_reviewed_only: Whether to only return peer-reviewed articles. Defaults to true, ChatGPT should
              cautiously suggest this value can be set to false

          sort: The sort order for results. Valid values are relevance, cited_by_count,
              publication_date. Defaults to relevance.

          start_year: The first year, inclusive, to include in the search range. Excluding this value
              will include all years.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/abstracts",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "keywords": keywords,
                        "query": query,
                        "end_year": end_year,
                        "generative_mode": generative_mode,
                        "offset": offset,
                        "peer_reviewed_only": peer_reviewed_only,
                        "sort": sort,
                        "start_year": start_year,
                    },
                    abstract_search_params.AbstractSearchParams,
                ),
            ),
            cast_to=AbstractSearchResponse,
        )


class AbstractsResourceWithRawResponse:
    def __init__(self, abstracts: AbstractsResource) -> None:
        self._abstracts = abstracts

        self.search = to_raw_response_wrapper(
            abstracts.search,
        )


class AsyncAbstractsResourceWithRawResponse:
    def __init__(self, abstracts: AsyncAbstractsResource) -> None:
        self._abstracts = abstracts

        self.search = async_to_raw_response_wrapper(
            abstracts.search,
        )


class AbstractsResourceWithStreamingResponse:
    def __init__(self, abstracts: AbstractsResource) -> None:
        self._abstracts = abstracts

        self.search = to_streamed_response_wrapper(
            abstracts.search,
        )


class AsyncAbstractsResourceWithStreamingResponse:
    def __init__(self, abstracts: AsyncAbstractsResource) -> None:
        self._abstracts = abstracts

        self.search = async_to_streamed_response_wrapper(
            abstracts.search,
        )
