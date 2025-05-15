# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import save_citation_retrieve_params
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
from ..types.save_citation_retrieve_response import SaveCitationRetrieveResponse

__all__ = ["SaveCitationResource", "AsyncSaveCitationResource"]


class SaveCitationResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SaveCitationResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#accessing-raw-response-data-eg-headers
        """
        return SaveCitationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SaveCitationResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#with_streaming_response
        """
        return SaveCitationResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        doi: str,
        zotero_api_key: str,
        zotero_user_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SaveCitationRetrieveResponse:
        """
        Saves a citation to the user's citation manager

        Args:
          doi: Digital Object Identifier (DOI) of the article

          zotero_api_key: Zotero API Key

          zotero_user_id: Zotero User ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/save-citation",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "doi": doi,
                        "zotero_api_key": zotero_api_key,
                        "zotero_user_id": zotero_user_id,
                    },
                    save_citation_retrieve_params.SaveCitationRetrieveParams,
                ),
            ),
            cast_to=SaveCitationRetrieveResponse,
        )


class AsyncSaveCitationResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSaveCitationResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSaveCitationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSaveCitationResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#with_streaming_response
        """
        return AsyncSaveCitationResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        doi: str,
        zotero_api_key: str,
        zotero_user_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SaveCitationRetrieveResponse:
        """
        Saves a citation to the user's citation manager

        Args:
          doi: Digital Object Identifier (DOI) of the article

          zotero_api_key: Zotero API Key

          zotero_user_id: Zotero User ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/save-citation",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "doi": doi,
                        "zotero_api_key": zotero_api_key,
                        "zotero_user_id": zotero_user_id,
                    },
                    save_citation_retrieve_params.SaveCitationRetrieveParams,
                ),
            ),
            cast_to=SaveCitationRetrieveResponse,
        )


class SaveCitationResourceWithRawResponse:
    def __init__(self, save_citation: SaveCitationResource) -> None:
        self._save_citation = save_citation

        self.retrieve = to_raw_response_wrapper(
            save_citation.retrieve,
        )


class AsyncSaveCitationResourceWithRawResponse:
    def __init__(self, save_citation: AsyncSaveCitationResource) -> None:
        self._save_citation = save_citation

        self.retrieve = async_to_raw_response_wrapper(
            save_citation.retrieve,
        )


class SaveCitationResourceWithStreamingResponse:
    def __init__(self, save_citation: SaveCitationResource) -> None:
        self._save_citation = save_citation

        self.retrieve = to_streamed_response_wrapper(
            save_citation.retrieve,
        )


class AsyncSaveCitationResourceWithStreamingResponse:
    def __init__(self, save_citation: AsyncSaveCitationResource) -> None:
        self._save_citation = save_citation

        self.retrieve = async_to_streamed_response_wrapper(
            save_citation.retrieve,
        )
