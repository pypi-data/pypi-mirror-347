# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

import httpx

from ..types import analyze_project_batch_analyze_params
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
from ..types.analyze_project_batch_analyze_response import AnalyzeProjectBatchAnalyzeResponse

__all__ = ["AnalyzeProjectResource", "AsyncAnalyzeProjectResource"]


class AnalyzeProjectResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AnalyzeProjectResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AnalyzeProjectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AnalyzeProjectResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#with_streaming_response
        """
        return AnalyzeProjectResourceWithStreamingResponse(self)

    def batch_analyze(
        self,
        *,
        analysis_mode: str,
        project_name: str,
        question: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AnalyzeProjectBatchAnalyzeResponse:
        """Accepts a project_name, and asks a question to every paper within.

        If no project
        is specified, uses a project named "GPT"

        Args:
          analysis_mode: The mode of analysis, options are 'comprehensive' and 'tabular'. Default to
              `tabular`.

          project_name: The name of the project to analyze.

          question: Questions to analyze within the project.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/analyze_project",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "analysis_mode": analysis_mode,
                        "project_name": project_name,
                        "question": question,
                    },
                    analyze_project_batch_analyze_params.AnalyzeProjectBatchAnalyzeParams,
                ),
            ),
            cast_to=AnalyzeProjectBatchAnalyzeResponse,
        )


class AsyncAnalyzeProjectResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAnalyzeProjectResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAnalyzeProjectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAnalyzeProjectResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#with_streaming_response
        """
        return AsyncAnalyzeProjectResourceWithStreamingResponse(self)

    async def batch_analyze(
        self,
        *,
        analysis_mode: str,
        project_name: str,
        question: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AnalyzeProjectBatchAnalyzeResponse:
        """Accepts a project_name, and asks a question to every paper within.

        If no project
        is specified, uses a project named "GPT"

        Args:
          analysis_mode: The mode of analysis, options are 'comprehensive' and 'tabular'. Default to
              `tabular`.

          project_name: The name of the project to analyze.

          question: Questions to analyze within the project.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/analyze_project",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "analysis_mode": analysis_mode,
                        "project_name": project_name,
                        "question": question,
                    },
                    analyze_project_batch_analyze_params.AnalyzeProjectBatchAnalyzeParams,
                ),
            ),
            cast_to=AnalyzeProjectBatchAnalyzeResponse,
        )


class AnalyzeProjectResourceWithRawResponse:
    def __init__(self, analyze_project: AnalyzeProjectResource) -> None:
        self._analyze_project = analyze_project

        self.batch_analyze = to_raw_response_wrapper(
            analyze_project.batch_analyze,
        )


class AsyncAnalyzeProjectResourceWithRawResponse:
    def __init__(self, analyze_project: AsyncAnalyzeProjectResource) -> None:
        self._analyze_project = analyze_project

        self.batch_analyze = async_to_raw_response_wrapper(
            analyze_project.batch_analyze,
        )


class AnalyzeProjectResourceWithStreamingResponse:
    def __init__(self, analyze_project: AnalyzeProjectResource) -> None:
        self._analyze_project = analyze_project

        self.batch_analyze = to_streamed_response_wrapper(
            analyze_project.batch_analyze,
        )


class AsyncAnalyzeProjectResourceWithStreamingResponse:
    def __init__(self, analyze_project: AsyncAnalyzeProjectResource) -> None:
        self._analyze_project = analyze_project

        self.batch_analyze = async_to_streamed_response_wrapper(
            analyze_project.batch_analyze,
        )
