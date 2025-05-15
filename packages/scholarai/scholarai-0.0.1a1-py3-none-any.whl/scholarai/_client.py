# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import is_given, get_async_library
from ._version import __version__
from .resources import (
    chat,
    patents,
    fulltext,
    question,
    abstracts,
    save_citation,
    add_to_project,
    create_project,
    analyze_project,
)
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError, ScholaraiError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "Scholarai",
    "AsyncScholarai",
    "Client",
    "AsyncClient",
]


class Scholarai(SyncAPIClient):
    chat: chat.ChatResource
    fulltext: fulltext.FulltextResource
    question: question.QuestionResource
    abstracts: abstracts.AbstractsResource
    patents: patents.PatentsResource
    save_citation: save_citation.SaveCitationResource
    add_to_project: add_to_project.AddToProjectResource
    create_project: create_project.CreateProjectResource
    analyze_project: analyze_project.AnalyzeProjectResource
    with_raw_response: ScholaraiWithRawResponse
    with_streaming_response: ScholaraiWithStreamedResponse

    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Scholarai client instance.

        This automatically infers the `api_key` argument from the `SCHOLARAI_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("SCHOLARAI_API_KEY")
        if api_key is None:
            raise ScholaraiError(
                "The api_key client option must be set either by passing api_key to the client or by setting the SCHOLARAI_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("SCHOLARAI_BASE_URL")
        if base_url is None:
            base_url = f"https://api.scholarai.io"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.chat = chat.ChatResource(self)
        self.fulltext = fulltext.FulltextResource(self)
        self.question = question.QuestionResource(self)
        self.abstracts = abstracts.AbstractsResource(self)
        self.patents = patents.PatentsResource(self)
        self.save_citation = save_citation.SaveCitationResource(self)
        self.add_to_project = add_to_project.AddToProjectResource(self)
        self.create_project = create_project.CreateProjectResource(self)
        self.analyze_project = analyze_project.AnalyzeProjectResource(self)
        self.with_raw_response = ScholaraiWithRawResponse(self)
        self.with_streaming_response = ScholaraiWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"x-scholarai-api-key": api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncScholarai(AsyncAPIClient):
    chat: chat.AsyncChatResource
    fulltext: fulltext.AsyncFulltextResource
    question: question.AsyncQuestionResource
    abstracts: abstracts.AsyncAbstractsResource
    patents: patents.AsyncPatentsResource
    save_citation: save_citation.AsyncSaveCitationResource
    add_to_project: add_to_project.AsyncAddToProjectResource
    create_project: create_project.AsyncCreateProjectResource
    analyze_project: analyze_project.AsyncAnalyzeProjectResource
    with_raw_response: AsyncScholaraiWithRawResponse
    with_streaming_response: AsyncScholaraiWithStreamedResponse

    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncScholarai client instance.

        This automatically infers the `api_key` argument from the `SCHOLARAI_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("SCHOLARAI_API_KEY")
        if api_key is None:
            raise ScholaraiError(
                "The api_key client option must be set either by passing api_key to the client or by setting the SCHOLARAI_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("SCHOLARAI_BASE_URL")
        if base_url is None:
            base_url = f"https://api.scholarai.io"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.chat = chat.AsyncChatResource(self)
        self.fulltext = fulltext.AsyncFulltextResource(self)
        self.question = question.AsyncQuestionResource(self)
        self.abstracts = abstracts.AsyncAbstractsResource(self)
        self.patents = patents.AsyncPatentsResource(self)
        self.save_citation = save_citation.AsyncSaveCitationResource(self)
        self.add_to_project = add_to_project.AsyncAddToProjectResource(self)
        self.create_project = create_project.AsyncCreateProjectResource(self)
        self.analyze_project = analyze_project.AsyncAnalyzeProjectResource(self)
        self.with_raw_response = AsyncScholaraiWithRawResponse(self)
        self.with_streaming_response = AsyncScholaraiWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"x-scholarai-api-key": api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class ScholaraiWithRawResponse:
    def __init__(self, client: Scholarai) -> None:
        self.chat = chat.ChatResourceWithRawResponse(client.chat)
        self.fulltext = fulltext.FulltextResourceWithRawResponse(client.fulltext)
        self.question = question.QuestionResourceWithRawResponse(client.question)
        self.abstracts = abstracts.AbstractsResourceWithRawResponse(client.abstracts)
        self.patents = patents.PatentsResourceWithRawResponse(client.patents)
        self.save_citation = save_citation.SaveCitationResourceWithRawResponse(client.save_citation)
        self.add_to_project = add_to_project.AddToProjectResourceWithRawResponse(client.add_to_project)
        self.create_project = create_project.CreateProjectResourceWithRawResponse(client.create_project)
        self.analyze_project = analyze_project.AnalyzeProjectResourceWithRawResponse(client.analyze_project)


class AsyncScholaraiWithRawResponse:
    def __init__(self, client: AsyncScholarai) -> None:
        self.chat = chat.AsyncChatResourceWithRawResponse(client.chat)
        self.fulltext = fulltext.AsyncFulltextResourceWithRawResponse(client.fulltext)
        self.question = question.AsyncQuestionResourceWithRawResponse(client.question)
        self.abstracts = abstracts.AsyncAbstractsResourceWithRawResponse(client.abstracts)
        self.patents = patents.AsyncPatentsResourceWithRawResponse(client.patents)
        self.save_citation = save_citation.AsyncSaveCitationResourceWithRawResponse(client.save_citation)
        self.add_to_project = add_to_project.AsyncAddToProjectResourceWithRawResponse(client.add_to_project)
        self.create_project = create_project.AsyncCreateProjectResourceWithRawResponse(client.create_project)
        self.analyze_project = analyze_project.AsyncAnalyzeProjectResourceWithRawResponse(client.analyze_project)


class ScholaraiWithStreamedResponse:
    def __init__(self, client: Scholarai) -> None:
        self.chat = chat.ChatResourceWithStreamingResponse(client.chat)
        self.fulltext = fulltext.FulltextResourceWithStreamingResponse(client.fulltext)
        self.question = question.QuestionResourceWithStreamingResponse(client.question)
        self.abstracts = abstracts.AbstractsResourceWithStreamingResponse(client.abstracts)
        self.patents = patents.PatentsResourceWithStreamingResponse(client.patents)
        self.save_citation = save_citation.SaveCitationResourceWithStreamingResponse(client.save_citation)
        self.add_to_project = add_to_project.AddToProjectResourceWithStreamingResponse(client.add_to_project)
        self.create_project = create_project.CreateProjectResourceWithStreamingResponse(client.create_project)
        self.analyze_project = analyze_project.AnalyzeProjectResourceWithStreamingResponse(client.analyze_project)


class AsyncScholaraiWithStreamedResponse:
    def __init__(self, client: AsyncScholarai) -> None:
        self.chat = chat.AsyncChatResourceWithStreamingResponse(client.chat)
        self.fulltext = fulltext.AsyncFulltextResourceWithStreamingResponse(client.fulltext)
        self.question = question.AsyncQuestionResourceWithStreamingResponse(client.question)
        self.abstracts = abstracts.AsyncAbstractsResourceWithStreamingResponse(client.abstracts)
        self.patents = patents.AsyncPatentsResourceWithStreamingResponse(client.patents)
        self.save_citation = save_citation.AsyncSaveCitationResourceWithStreamingResponse(client.save_citation)
        self.add_to_project = add_to_project.AsyncAddToProjectResourceWithStreamingResponse(client.add_to_project)
        self.create_project = create_project.AsyncCreateProjectResourceWithStreamingResponse(client.create_project)
        self.analyze_project = analyze_project.AsyncAnalyzeProjectResourceWithStreamingResponse(client.analyze_project)


Client = Scholarai

AsyncClient = AsyncScholarai
