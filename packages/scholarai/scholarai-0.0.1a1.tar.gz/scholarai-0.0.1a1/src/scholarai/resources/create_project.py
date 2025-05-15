# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import create_project_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
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

__all__ = ["CreateProjectResource", "AsyncCreateProjectResource"]


class CreateProjectResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CreateProjectResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#accessing-raw-response-data-eg-headers
        """
        return CreateProjectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CreateProjectResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#with_streaming_response
        """
        return CreateProjectResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        project_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Creates a project using query params

        Args:
          project_name: Desired name for the project

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/api/create_project",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"project_name": project_name}, create_project_create_params.CreateProjectCreateParams
                ),
            ),
            cast_to=NoneType,
        )


class AsyncCreateProjectResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCreateProjectResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCreateProjectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCreateProjectResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#with_streaming_response
        """
        return AsyncCreateProjectResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        project_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Creates a project using query params

        Args:
          project_name: Desired name for the project

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/api/create_project",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"project_name": project_name}, create_project_create_params.CreateProjectCreateParams
                ),
            ),
            cast_to=NoneType,
        )


class CreateProjectResourceWithRawResponse:
    def __init__(self, create_project: CreateProjectResource) -> None:
        self._create_project = create_project

        self.create = to_raw_response_wrapper(
            create_project.create,
        )


class AsyncCreateProjectResourceWithRawResponse:
    def __init__(self, create_project: AsyncCreateProjectResource) -> None:
        self._create_project = create_project

        self.create = async_to_raw_response_wrapper(
            create_project.create,
        )


class CreateProjectResourceWithStreamingResponse:
    def __init__(self, create_project: CreateProjectResource) -> None:
        self._create_project = create_project

        self.create = to_streamed_response_wrapper(
            create_project.create,
        )


class AsyncCreateProjectResourceWithStreamingResponse:
    def __init__(self, create_project: AsyncCreateProjectResource) -> None:
        self._create_project = create_project

        self.create = async_to_streamed_response_wrapper(
            create_project.create,
        )
