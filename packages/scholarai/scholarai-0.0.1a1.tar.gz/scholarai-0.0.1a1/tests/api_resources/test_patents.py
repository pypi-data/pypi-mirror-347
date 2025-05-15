# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scholarai import Scholarai, AsyncScholarai
from tests.utils import assert_matches_type
from scholarai.types import PatentListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPatents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Scholarai) -> None:
        patent = client.patents.list(
            full_user_prompt="full_user_prompt",
            keywords="keywords",
            query="query",
        )
        assert_matches_type(PatentListResponse, patent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: Scholarai) -> None:
        patent = client.patents.list(
            full_user_prompt="full_user_prompt",
            keywords="keywords",
            query="query",
            end_year="end_year",
            generative_mode="generative_mode",
            offset="offset",
            peer_reviewed_only="peer_reviewed_only",
            sort="sort",
            start_year="start_year",
        )
        assert_matches_type(PatentListResponse, patent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Scholarai) -> None:
        response = client.patents.with_raw_response.list(
            full_user_prompt="full_user_prompt",
            keywords="keywords",
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        patent = response.parse()
        assert_matches_type(PatentListResponse, patent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Scholarai) -> None:
        with client.patents.with_streaming_response.list(
            full_user_prompt="full_user_prompt",
            keywords="keywords",
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            patent = response.parse()
            assert_matches_type(PatentListResponse, patent, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPatents:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncScholarai) -> None:
        patent = await async_client.patents.list(
            full_user_prompt="full_user_prompt",
            keywords="keywords",
            query="query",
        )
        assert_matches_type(PatentListResponse, patent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncScholarai) -> None:
        patent = await async_client.patents.list(
            full_user_prompt="full_user_prompt",
            keywords="keywords",
            query="query",
            end_year="end_year",
            generative_mode="generative_mode",
            offset="offset",
            peer_reviewed_only="peer_reviewed_only",
            sort="sort",
            start_year="start_year",
        )
        assert_matches_type(PatentListResponse, patent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncScholarai) -> None:
        response = await async_client.patents.with_raw_response.list(
            full_user_prompt="full_user_prompt",
            keywords="keywords",
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        patent = await response.parse()
        assert_matches_type(PatentListResponse, patent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncScholarai) -> None:
        async with async_client.patents.with_streaming_response.list(
            full_user_prompt="full_user_prompt",
            keywords="keywords",
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            patent = await response.parse()
            assert_matches_type(PatentListResponse, patent, path=["response"])

        assert cast(Any, response.is_closed) is True
