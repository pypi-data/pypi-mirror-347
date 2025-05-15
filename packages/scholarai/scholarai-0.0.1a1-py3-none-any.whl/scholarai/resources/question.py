# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import question_ask_params
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

__all__ = ["QuestionResource", "AsyncQuestionResource"]


class QuestionResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> QuestionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#accessing-raw-response-data-eg-headers
        """
        return QuestionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> QuestionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#with_streaming_response
        """
        return QuestionResourceWithStreamingResponse(self)

    def ask(
        self,
        *,
        pdf_id: str,
        question: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaperContent:
        """
        Uses embedding model to find section of PDF most relevant for answering a
        question :param pdf_url: the url :param question: the question :return: the
        chunk most relevant to answering that question and its source

        Args:
          pdf_id: id for PDF. Must begin with be one of `PDF_URL:some.url.com` or `PROJ:some_path`

          question: The user question. Must be in English.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/question",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "pdf_id": pdf_id,
                        "question": question,
                    },
                    question_ask_params.QuestionAskParams,
                ),
            ),
            cast_to=PaperContent,
        )


class AsyncQuestionResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncQuestionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncQuestionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncQuestionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#with_streaming_response
        """
        return AsyncQuestionResourceWithStreamingResponse(self)

    async def ask(
        self,
        *,
        pdf_id: str,
        question: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaperContent:
        """
        Uses embedding model to find section of PDF most relevant for answering a
        question :param pdf_url: the url :param question: the question :return: the
        chunk most relevant to answering that question and its source

        Args:
          pdf_id: id for PDF. Must begin with be one of `PDF_URL:some.url.com` or `PROJ:some_path`

          question: The user question. Must be in English.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/question",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "pdf_id": pdf_id,
                        "question": question,
                    },
                    question_ask_params.QuestionAskParams,
                ),
            ),
            cast_to=PaperContent,
        )


class QuestionResourceWithRawResponse:
    def __init__(self, question: QuestionResource) -> None:
        self._question = question

        self.ask = to_raw_response_wrapper(
            question.ask,
        )


class AsyncQuestionResourceWithRawResponse:
    def __init__(self, question: AsyncQuestionResource) -> None:
        self._question = question

        self.ask = async_to_raw_response_wrapper(
            question.ask,
        )


class QuestionResourceWithStreamingResponse:
    def __init__(self, question: QuestionResource) -> None:
        self._question = question

        self.ask = to_streamed_response_wrapper(
            question.ask,
        )


class AsyncQuestionResourceWithStreamingResponse:
    def __init__(self, question: AsyncQuestionResource) -> None:
        self._question = question

        self.ask = async_to_streamed_response_wrapper(
            question.ask,
        )
