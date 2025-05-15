# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scholarai import Scholarai, AsyncScholarai
from tests.utils import assert_matches_type
from scholarai.types import AbstractSearchResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAbstracts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_search(self, client: Scholarai) -> None:
        abstract = client.abstracts.search(
            keywords="keywords",
            query="query",
        )
        assert_matches_type(AbstractSearchResponse, abstract, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_search_with_all_params(self, client: Scholarai) -> None:
        abstract = client.abstracts.search(
            keywords="keywords",
            query="query",
            end_year=0,
            generative_mode=True,
            offset=0,
            peer_reviewed_only=True,
            sort="sort",
            start_year=0,
        )
        assert_matches_type(AbstractSearchResponse, abstract, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_search(self, client: Scholarai) -> None:
        response = client.abstracts.with_raw_response.search(
            keywords="keywords",
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        abstract = response.parse()
        assert_matches_type(AbstractSearchResponse, abstract, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_search(self, client: Scholarai) -> None:
        with client.abstracts.with_streaming_response.search(
            keywords="keywords",
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            abstract = response.parse()
            assert_matches_type(AbstractSearchResponse, abstract, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAbstracts:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_search(self, async_client: AsyncScholarai) -> None:
        abstract = await async_client.abstracts.search(
            keywords="keywords",
            query="query",
        )
        assert_matches_type(AbstractSearchResponse, abstract, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncScholarai) -> None:
        abstract = await async_client.abstracts.search(
            keywords="keywords",
            query="query",
            end_year=0,
            generative_mode=True,
            offset=0,
            peer_reviewed_only=True,
            sort="sort",
            start_year=0,
        )
        assert_matches_type(AbstractSearchResponse, abstract, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_search(self, async_client: AsyncScholarai) -> None:
        response = await async_client.abstracts.with_raw_response.search(
            keywords="keywords",
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        abstract = await response.parse()
        assert_matches_type(AbstractSearchResponse, abstract, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncScholarai) -> None:
        async with async_client.abstracts.with_streaming_response.search(
            keywords="keywords",
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            abstract = await response.parse()
            assert_matches_type(AbstractSearchResponse, abstract, path=["response"])

        assert cast(Any, response.is_closed) is True
