# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scholarai import Scholarai, AsyncScholarai
from tests.utils import assert_matches_type
from scholarai.types import PaperContent

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFulltext:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Scholarai) -> None:
        fulltext = client.fulltext.retrieve(
            pdf_id="pdf_id",
        )
        assert_matches_type(PaperContent, fulltext, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Scholarai) -> None:
        fulltext = client.fulltext.retrieve(
            pdf_id="pdf_id",
            chunk=0,
        )
        assert_matches_type(PaperContent, fulltext, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Scholarai) -> None:
        response = client.fulltext.with_raw_response.retrieve(
            pdf_id="pdf_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fulltext = response.parse()
        assert_matches_type(PaperContent, fulltext, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Scholarai) -> None:
        with client.fulltext.with_streaming_response.retrieve(
            pdf_id="pdf_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fulltext = response.parse()
            assert_matches_type(PaperContent, fulltext, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncFulltext:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncScholarai) -> None:
        fulltext = await async_client.fulltext.retrieve(
            pdf_id="pdf_id",
        )
        assert_matches_type(PaperContent, fulltext, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncScholarai) -> None:
        fulltext = await async_client.fulltext.retrieve(
            pdf_id="pdf_id",
            chunk=0,
        )
        assert_matches_type(PaperContent, fulltext, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncScholarai) -> None:
        response = await async_client.fulltext.with_raw_response.retrieve(
            pdf_id="pdf_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fulltext = await response.parse()
        assert_matches_type(PaperContent, fulltext, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncScholarai) -> None:
        async with async_client.fulltext.with_streaming_response.retrieve(
            pdf_id="pdf_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fulltext = await response.parse()
            assert_matches_type(PaperContent, fulltext, path=["response"])

        assert cast(Any, response.is_closed) is True
