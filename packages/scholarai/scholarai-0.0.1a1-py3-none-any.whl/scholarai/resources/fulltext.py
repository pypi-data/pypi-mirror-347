# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import fulltext_retrieve_params
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
from ..types.paper_content import PaperContent

__all__ = ["FulltextResource", "AsyncFulltextResource"]


class FulltextResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FulltextResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#accessing-raw-response-data-eg-headers
        """
        return FulltextResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FulltextResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#with_streaming_response
        """
        return FulltextResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        pdf_id: str,
        chunk: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaperContent:
        """Retrieves the full text of an article by its pdf_url.

        May use a cached entry or
        read from other data sources before trying PDF parsing. :param pdf_url: the url
        of the pdf :param chunk: the chunk number to retrieve :return: the chunk of the
        full text requested with the page number and total number of pages

        Args:
          pdf_id: id for PDF. Must begin with be one of `PDF_URL:some.url.com` or `PROJ:some_path`

          chunk: chunk number to retrieve, defaults to 1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/fulltext",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "pdf_id": pdf_id,
                        "chunk": chunk,
                    },
                    fulltext_retrieve_params.FulltextRetrieveParams,
                ),
            ),
            cast_to=PaperContent,
        )


class AsyncFulltextResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFulltextResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncFulltextResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFulltextResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#with_streaming_response
        """
        return AsyncFulltextResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        pdf_id: str,
        chunk: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaperContent:
        """Retrieves the full text of an article by its pdf_url.

        May use a cached entry or
        read from other data sources before trying PDF parsing. :param pdf_url: the url
        of the pdf :param chunk: the chunk number to retrieve :return: the chunk of the
        full text requested with the page number and total number of pages

        Args:
          pdf_id: id for PDF. Must begin with be one of `PDF_URL:some.url.com` or `PROJ:some_path`

          chunk: chunk number to retrieve, defaults to 1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/fulltext",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "pdf_id": pdf_id,
                        "chunk": chunk,
                    },
                    fulltext_retrieve_params.FulltextRetrieveParams,
                ),
            ),
            cast_to=PaperContent,
        )


class FulltextResourceWithRawResponse:
    def __init__(self, fulltext: FulltextResource) -> None:
        self._fulltext = fulltext

        self.retrieve = to_raw_response_wrapper(
            fulltext.retrieve,
        )


class AsyncFulltextResourceWithRawResponse:
    def __init__(self, fulltext: AsyncFulltextResource) -> None:
        self._fulltext = fulltext

        self.retrieve = async_to_raw_response_wrapper(
            fulltext.retrieve,
        )


class FulltextResourceWithStreamingResponse:
    def __init__(self, fulltext: FulltextResource) -> None:
        self._fulltext = fulltext

        self.retrieve = to_streamed_response_wrapper(
            fulltext.retrieve,
        )


class AsyncFulltextResourceWithStreamingResponse:
    def __init__(self, fulltext: AsyncFulltextResource) -> None:
        self._fulltext = fulltext

        self.retrieve = async_to_streamed_response_wrapper(
            fulltext.retrieve,
        )
