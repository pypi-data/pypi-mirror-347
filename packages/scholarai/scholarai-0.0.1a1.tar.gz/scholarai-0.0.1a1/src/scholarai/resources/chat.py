# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..types import chat_create_completion_params
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

__all__ = ["ChatResource", "AsyncChatResource"]


class ChatResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ChatResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#accessing-raw-response-data-eg-headers
        """
        return ChatResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChatResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#with_streaming_response
        """
        return ChatResourceWithStreamingResponse(self)

    def create_completion(
        self,
        *,
        messages: Iterable[chat_create_completion_params.Message] | NotGiven = NOT_GIVEN,
        model: str | NotGiven = NOT_GIVEN,
        stream: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Mimics the input and output to the OpenAI Chat Completion API:
        https://platform.openai.com/docs/api-reference/chat/create

        Args:
          model: Model being used. Currently ignored and defaults to "scholarai" with GPT4-turbo

          stream: Whether or not to stream the response. Streaming is recommended!

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/api/chat/completions",
            body=maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                    "stream": stream,
                },
                chat_create_completion_params.ChatCreateCompletionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncChatResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncChatResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncChatResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChatResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Project-Scholar-AI/scholarai-sdk-python#with_streaming_response
        """
        return AsyncChatResourceWithStreamingResponse(self)

    async def create_completion(
        self,
        *,
        messages: Iterable[chat_create_completion_params.Message] | NotGiven = NOT_GIVEN,
        model: str | NotGiven = NOT_GIVEN,
        stream: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Mimics the input and output to the OpenAI Chat Completion API:
        https://platform.openai.com/docs/api-reference/chat/create

        Args:
          model: Model being used. Currently ignored and defaults to "scholarai" with GPT4-turbo

          stream: Whether or not to stream the response. Streaming is recommended!

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/api/chat/completions",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                    "stream": stream,
                },
                chat_create_completion_params.ChatCreateCompletionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class ChatResourceWithRawResponse:
    def __init__(self, chat: ChatResource) -> None:
        self._chat = chat

        self.create_completion = to_raw_response_wrapper(
            chat.create_completion,
        )


class AsyncChatResourceWithRawResponse:
    def __init__(self, chat: AsyncChatResource) -> None:
        self._chat = chat

        self.create_completion = async_to_raw_response_wrapper(
            chat.create_completion,
        )


class ChatResourceWithStreamingResponse:
    def __init__(self, chat: ChatResource) -> None:
        self._chat = chat

        self.create_completion = to_streamed_response_wrapper(
            chat.create_completion,
        )


class AsyncChatResourceWithStreamingResponse:
    def __init__(self, chat: AsyncChatResource) -> None:
        self._chat = chat

        self.create_completion = async_to_streamed_response_wrapper(
            chat.create_completion,
        )
