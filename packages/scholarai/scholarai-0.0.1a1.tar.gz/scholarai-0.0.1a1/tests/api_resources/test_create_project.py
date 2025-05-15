# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scholarai import Scholarai, AsyncScholarai

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCreateProject:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Scholarai) -> None:
        create_project = client.create_project.create(
            project_name="project_name",
        )
        assert create_project is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Scholarai) -> None:
        response = client.create_project.with_raw_response.create(
            project_name="project_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        create_project = response.parse()
        assert create_project is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Scholarai) -> None:
        with client.create_project.with_streaming_response.create(
            project_name="project_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            create_project = response.parse()
            assert create_project is None

        assert cast(Any, response.is_closed) is True


class TestAsyncCreateProject:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncScholarai) -> None:
        create_project = await async_client.create_project.create(
            project_name="project_name",
        )
        assert create_project is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncScholarai) -> None:
        response = await async_client.create_project.with_raw_response.create(
            project_name="project_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        create_project = await response.parse()
        assert create_project is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncScholarai) -> None:
        async with async_client.create_project.with_streaming_response.create(
            project_name="project_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            create_project = await response.parse()
            assert create_project is None

        assert cast(Any, response.is_closed) is True
