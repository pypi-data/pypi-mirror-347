# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import add_to_project_create_params, add_to_project_retrieve_params
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
from ..types.add_to_project_create_response import AddToProjectCreateResponse
from ..types.add_to_project_retrieve_response import AddToProjectRetrieveResponse

__all__ = ["AddToProjectResource", "AsyncAddToProjectResource"]


class AddToProjectResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AddToProjectResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AddToProjectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AddToProjectResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#with_streaming_response
        """
        return AddToProjectResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        paper_id: str,
        project_id: str | NotGiven = NOT_GIVEN,
        project_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AddToProjectCreateResponse:
        """
        Accept a PDF url or multipart form-data containing a file, and add it to the
        user's project in the database. If no project is specified, add it to a project
        named "GPT"

        Args:
          paper_id: Identifier of the paper to add, must be of the format
              <identifier_type>:<identifier_value>. Identifier type can be one of DOI, PMID,
              SS_ID, ARXIV, MAG, ACL, or PMCID.

          project_id: The project ID to which the items are being added. Default to 'gpt'

          project_name: The project name to which the items are being added. Alternative to project_id

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/add_to_project",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "paper_id": paper_id,
                        "project_id": project_id,
                        "project_name": project_name,
                    },
                    add_to_project_create_params.AddToProjectCreateParams,
                ),
            ),
            cast_to=AddToProjectCreateResponse,
        )

    def retrieve(
        self,
        *,
        paper_id: str,
        project_id: str | NotGiven = NOT_GIVEN,
        project_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AddToProjectRetrieveResponse:
        """
        Accept a PDF url or multipart form-data containing a file, and add it to the
        user's project in the database. If no project is specified, add it to a project
        named "GPT"

        Args:
          paper_id: Identifier of the paper to add, must be of the format
              <identifier_type>:<identifier_value>. Identifier type can be one of DOI, PMID,
              SS_ID, ARXIV, MAG, ACL, or PMCID.

          project_id: The project ID to which the items are being added. Default to 'gpt'

          project_name: The project name to which the items are being added. Alternative to project_id

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/add_to_project",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "paper_id": paper_id,
                        "project_id": project_id,
                        "project_name": project_name,
                    },
                    add_to_project_retrieve_params.AddToProjectRetrieveParams,
                ),
            ),
            cast_to=AddToProjectRetrieveResponse,
        )


class AsyncAddToProjectResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAddToProjectResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAddToProjectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAddToProjectResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#with_streaming_response
        """
        return AsyncAddToProjectResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        paper_id: str,
        project_id: str | NotGiven = NOT_GIVEN,
        project_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AddToProjectCreateResponse:
        """
        Accept a PDF url or multipart form-data containing a file, and add it to the
        user's project in the database. If no project is specified, add it to a project
        named "GPT"

        Args:
          paper_id: Identifier of the paper to add, must be of the format
              <identifier_type>:<identifier_value>. Identifier type can be one of DOI, PMID,
              SS_ID, ARXIV, MAG, ACL, or PMCID.

          project_id: The project ID to which the items are being added. Default to 'gpt'

          project_name: The project name to which the items are being added. Alternative to project_id

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/add_to_project",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "paper_id": paper_id,
                        "project_id": project_id,
                        "project_name": project_name,
                    },
                    add_to_project_create_params.AddToProjectCreateParams,
                ),
            ),
            cast_to=AddToProjectCreateResponse,
        )

    async def retrieve(
        self,
        *,
        paper_id: str,
        project_id: str | NotGiven = NOT_GIVEN,
        project_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AddToProjectRetrieveResponse:
        """
        Accept a PDF url or multipart form-data containing a file, and add it to the
        user's project in the database. If no project is specified, add it to a project
        named "GPT"

        Args:
          paper_id: Identifier of the paper to add, must be of the format
              <identifier_type>:<identifier_value>. Identifier type can be one of DOI, PMID,
              SS_ID, ARXIV, MAG, ACL, or PMCID.

          project_id: The project ID to which the items are being added. Default to 'gpt'

          project_name: The project name to which the items are being added. Alternative to project_id

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/add_to_project",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "paper_id": paper_id,
                        "project_id": project_id,
                        "project_name": project_name,
                    },
                    add_to_project_retrieve_params.AddToProjectRetrieveParams,
                ),
            ),
            cast_to=AddToProjectRetrieveResponse,
        )


class AddToProjectResourceWithRawResponse:
    def __init__(self, add_to_project: AddToProjectResource) -> None:
        self._add_to_project = add_to_project

        self.create = to_raw_response_wrapper(
            add_to_project.create,
        )
        self.retrieve = to_raw_response_wrapper(
            add_to_project.retrieve,
        )


class AsyncAddToProjectResourceWithRawResponse:
    def __init__(self, add_to_project: AsyncAddToProjectResource) -> None:
        self._add_to_project = add_to_project

        self.create = async_to_raw_response_wrapper(
            add_to_project.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            add_to_project.retrieve,
        )


class AddToProjectResourceWithStreamingResponse:
    def __init__(self, add_to_project: AddToProjectResource) -> None:
        self._add_to_project = add_to_project

        self.create = to_streamed_response_wrapper(
            add_to_project.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            add_to_project.retrieve,
        )


class AsyncAddToProjectResourceWithStreamingResponse:
    def __init__(self, add_to_project: AsyncAddToProjectResource) -> None:
        self._add_to_project = add_to_project

        self.create = async_to_streamed_response_wrapper(
            add_to_project.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            add_to_project.retrieve,
        )
