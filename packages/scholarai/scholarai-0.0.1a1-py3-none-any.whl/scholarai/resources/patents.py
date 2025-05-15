# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import patent_list_params
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
from ..types.patent_list_response import PatentListResponse

__all__ = ["PatentsResource", "AsyncPatentsResource"]


class PatentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PatentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#accessing-raw-response-data-eg-headers
        """
        return PatentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PatentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#with_streaming_response
        """
        return PatentsResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        full_user_prompt: str,
        keywords: str,
        query: str,
        end_year: str | NotGiven = NOT_GIVEN,
        generative_mode: str | NotGiven = NOT_GIVEN,
        offset: str | NotGiven = NOT_GIVEN,
        peer_reviewed_only: str | NotGiven = NOT_GIVEN,
        sort: str | NotGiven = NOT_GIVEN,
        start_year: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PatentListResponse:
        """
        Get relevant patents by searching 2-6 relevant keywords.

        Args:
          full_user_prompt: The entirety of the user request, directly quoted.

          keywords: Keywords of inquiry which should appear in article. Must be in English.

          query: The user query. If the user asks for a specific patent, you MUST hit the API
              using escaped quotation marks

          end_year: The last year, inclusive, to include in the search range. Excluding this value
              will include all years.

          generative_mode: Boolean "true" or "false" to enable generative mode. If enabled, collate
              responses using markdown to render in-text citations to the source's url if
              available. Set this to true by default.

          offset: The offset of the first result to return. Defaults to 0.

          peer_reviewed_only: Whether to only return peer reviewed articles. Defaults to true, ChatGPT should
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
            "/api/patents",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "full_user_prompt": full_user_prompt,
                        "keywords": keywords,
                        "query": query,
                        "end_year": end_year,
                        "generative_mode": generative_mode,
                        "offset": offset,
                        "peer_reviewed_only": peer_reviewed_only,
                        "sort": sort,
                        "start_year": start_year,
                    },
                    patent_list_params.PatentListParams,
                ),
            ),
            cast_to=PatentListResponse,
        )


class AsyncPatentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPatentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPatentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPatentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#with_streaming_response
        """
        return AsyncPatentsResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        full_user_prompt: str,
        keywords: str,
        query: str,
        end_year: str | NotGiven = NOT_GIVEN,
        generative_mode: str | NotGiven = NOT_GIVEN,
        offset: str | NotGiven = NOT_GIVEN,
        peer_reviewed_only: str | NotGiven = NOT_GIVEN,
        sort: str | NotGiven = NOT_GIVEN,
        start_year: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PatentListResponse:
        """
        Get relevant patents by searching 2-6 relevant keywords.

        Args:
          full_user_prompt: The entirety of the user request, directly quoted.

          keywords: Keywords of inquiry which should appear in article. Must be in English.

          query: The user query. If the user asks for a specific patent, you MUST hit the API
              using escaped quotation marks

          end_year: The last year, inclusive, to include in the search range. Excluding this value
              will include all years.

          generative_mode: Boolean "true" or "false" to enable generative mode. If enabled, collate
              responses using markdown to render in-text citations to the source's url if
              available. Set this to true by default.

          offset: The offset of the first result to return. Defaults to 0.

          peer_reviewed_only: Whether to only return peer reviewed articles. Defaults to true, ChatGPT should
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
            "/api/patents",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "full_user_prompt": full_user_prompt,
                        "keywords": keywords,
                        "query": query,
                        "end_year": end_year,
                        "generative_mode": generative_mode,
                        "offset": offset,
                        "peer_reviewed_only": peer_reviewed_only,
                        "sort": sort,
                        "start_year": start_year,
                    },
                    patent_list_params.PatentListParams,
                ),
            ),
            cast_to=PatentListResponse,
        )


class PatentsResourceWithRawResponse:
    def __init__(self, patents: PatentsResource) -> None:
        self._patents = patents

        self.list = to_raw_response_wrapper(
            patents.list,
        )


class AsyncPatentsResourceWithRawResponse:
    def __init__(self, patents: AsyncPatentsResource) -> None:
        self._patents = patents

        self.list = async_to_raw_response_wrapper(
            patents.list,
        )


class PatentsResourceWithStreamingResponse:
    def __init__(self, patents: PatentsResource) -> None:
        self._patents = patents

        self.list = to_streamed_response_wrapper(
            patents.list,
        )


class AsyncPatentsResourceWithStreamingResponse:
    def __init__(self, patents: AsyncPatentsResource) -> None:
        self._patents = patents

        self.list = async_to_streamed_response_wrapper(
            patents.list,
        )
