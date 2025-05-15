# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scholarai import Scholarai, AsyncScholarai
from tests.utils import assert_matches_type
from scholarai.types import SaveCitationRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSaveCitation:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Scholarai) -> None:
        save_citation = client.save_citation.retrieve(
            doi="doi",
            zotero_api_key="zotero_api_key",
            zotero_user_id="zotero_user_id",
        )
        assert_matches_type(SaveCitationRetrieveResponse, save_citation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Scholarai) -> None:
        response = client.save_citation.with_raw_response.retrieve(
            doi="doi",
            zotero_api_key="zotero_api_key",
            zotero_user_id="zotero_user_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        save_citation = response.parse()
        assert_matches_type(SaveCitationRetrieveResponse, save_citation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Scholarai) -> None:
        with client.save_citation.with_streaming_response.retrieve(
            doi="doi",
            zotero_api_key="zotero_api_key",
            zotero_user_id="zotero_user_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            save_citation = response.parse()
            assert_matches_type(SaveCitationRetrieveResponse, save_citation, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSaveCitation:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncScholarai) -> None:
        save_citation = await async_client.save_citation.retrieve(
            doi="doi",
            zotero_api_key="zotero_api_key",
            zotero_user_id="zotero_user_id",
        )
        assert_matches_type(SaveCitationRetrieveResponse, save_citation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncScholarai) -> None:
        response = await async_client.save_citation.with_raw_response.retrieve(
            doi="doi",
            zotero_api_key="zotero_api_key",
            zotero_user_id="zotero_user_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        save_citation = await response.parse()
        assert_matches_type(SaveCitationRetrieveResponse, save_citation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncScholarai) -> None:
        async with async_client.save_citation.with_streaming_response.retrieve(
            doi="doi",
            zotero_api_key="zotero_api_key",
            zotero_user_id="zotero_user_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            save_citation = await response.parse()
            assert_matches_type(SaveCitationRetrieveResponse, save_citation, path=["response"])

        assert cast(Any, response.is_closed) is True
