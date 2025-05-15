# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scholarai import Scholarai, AsyncScholarai
from tests.utils import assert_matches_type
from scholarai.types import (
    AddToProjectCreateResponse,
    AddToProjectRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAddToProject:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Scholarai) -> None:
        add_to_project = client.add_to_project.create(
            paper_id="paper_id",
        )
        assert_matches_type(AddToProjectCreateResponse, add_to_project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: Scholarai) -> None:
        add_to_project = client.add_to_project.create(
            paper_id="paper_id",
            project_id="project_id",
            project_name="project_name",
        )
        assert_matches_type(AddToProjectCreateResponse, add_to_project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Scholarai) -> None:
        response = client.add_to_project.with_raw_response.create(
            paper_id="paper_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        add_to_project = response.parse()
        assert_matches_type(AddToProjectCreateResponse, add_to_project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Scholarai) -> None:
        with client.add_to_project.with_streaming_response.create(
            paper_id="paper_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            add_to_project = response.parse()
            assert_matches_type(AddToProjectCreateResponse, add_to_project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Scholarai) -> None:
        add_to_project = client.add_to_project.retrieve(
            paper_id="paper_id",
        )
        assert_matches_type(AddToProjectRetrieveResponse, add_to_project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Scholarai) -> None:
        add_to_project = client.add_to_project.retrieve(
            paper_id="paper_id",
            project_id="project_id",
            project_name="project_name",
        )
        assert_matches_type(AddToProjectRetrieveResponse, add_to_project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Scholarai) -> None:
        response = client.add_to_project.with_raw_response.retrieve(
            paper_id="paper_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        add_to_project = response.parse()
        assert_matches_type(AddToProjectRetrieveResponse, add_to_project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Scholarai) -> None:
        with client.add_to_project.with_streaming_response.retrieve(
            paper_id="paper_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            add_to_project = response.parse()
            assert_matches_type(AddToProjectRetrieveResponse, add_to_project, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAddToProject:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncScholarai) -> None:
        add_to_project = await async_client.add_to_project.create(
            paper_id="paper_id",
        )
        assert_matches_type(AddToProjectCreateResponse, add_to_project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncScholarai) -> None:
        add_to_project = await async_client.add_to_project.create(
            paper_id="paper_id",
            project_id="project_id",
            project_name="project_name",
        )
        assert_matches_type(AddToProjectCreateResponse, add_to_project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncScholarai) -> None:
        response = await async_client.add_to_project.with_raw_response.create(
            paper_id="paper_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        add_to_project = await response.parse()
        assert_matches_type(AddToProjectCreateResponse, add_to_project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncScholarai) -> None:
        async with async_client.add_to_project.with_streaming_response.create(
            paper_id="paper_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            add_to_project = await response.parse()
            assert_matches_type(AddToProjectCreateResponse, add_to_project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncScholarai) -> None:
        add_to_project = await async_client.add_to_project.retrieve(
            paper_id="paper_id",
        )
        assert_matches_type(AddToProjectRetrieveResponse, add_to_project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncScholarai) -> None:
        add_to_project = await async_client.add_to_project.retrieve(
            paper_id="paper_id",
            project_id="project_id",
            project_name="project_name",
        )
        assert_matches_type(AddToProjectRetrieveResponse, add_to_project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncScholarai) -> None:
        response = await async_client.add_to_project.with_raw_response.retrieve(
            paper_id="paper_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        add_to_project = await response.parse()
        assert_matches_type(AddToProjectRetrieveResponse, add_to_project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncScholarai) -> None:
        async with async_client.add_to_project.with_streaming_response.retrieve(
            paper_id="paper_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            add_to_project = await response.parse()
            assert_matches_type(AddToProjectRetrieveResponse, add_to_project, path=["response"])

        assert cast(Any, response.is_closed) is True
