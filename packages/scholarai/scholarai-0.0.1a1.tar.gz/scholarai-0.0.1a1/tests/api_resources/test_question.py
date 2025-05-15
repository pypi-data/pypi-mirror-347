# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scholarai import Scholarai, AsyncScholarai
from tests.utils import assert_matches_type
from scholarai.types import PaperContent

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestQuestion:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_ask(self, client: Scholarai) -> None:
        question = client.question.ask(
            pdf_id="pdf_id",
            question="question",
        )
        assert_matches_type(PaperContent, question, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_ask(self, client: Scholarai) -> None:
        response = client.question.with_raw_response.ask(
            pdf_id="pdf_id",
            question="question",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = response.parse()
        assert_matches_type(PaperContent, question, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_ask(self, client: Scholarai) -> None:
        with client.question.with_streaming_response.ask(
            pdf_id="pdf_id",
            question="question",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = response.parse()
            assert_matches_type(PaperContent, question, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncQuestion:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_ask(self, async_client: AsyncScholarai) -> None:
        question = await async_client.question.ask(
            pdf_id="pdf_id",
            question="question",
        )
        assert_matches_type(PaperContent, question, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_ask(self, async_client: AsyncScholarai) -> None:
        response = await async_client.question.with_raw_response.ask(
            pdf_id="pdf_id",
            question="question",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = await response.parse()
        assert_matches_type(PaperContent, question, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_ask(self, async_client: AsyncScholarai) -> None:
        async with async_client.question.with_streaming_response.ask(
            pdf_id="pdf_id",
            question="question",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = await response.parse()
            assert_matches_type(PaperContent, question, path=["response"])

        assert cast(Any, response.is_closed) is True
