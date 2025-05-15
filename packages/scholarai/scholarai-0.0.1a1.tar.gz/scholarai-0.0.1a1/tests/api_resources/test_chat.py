# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scholarai import Scholarai, AsyncScholarai

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChat:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_completion(self, client: Scholarai) -> None:
        chat = client.chat.create_completion()
        assert chat is None

    @pytest.mark.skip()
    @parametrize
    def test_method_create_completion_with_all_params(self, client: Scholarai) -> None:
        chat = client.chat.create_completion(
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            model="model",
            stream=True,
        )
        assert chat is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_completion(self, client: Scholarai) -> None:
        response = client.chat.with_raw_response.create_completion()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert chat is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_completion(self, client: Scholarai) -> None:
        with client.chat.with_streaming_response.create_completion() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert chat is None

        assert cast(Any, response.is_closed) is True


class TestAsyncChat:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_completion(self, async_client: AsyncScholarai) -> None:
        chat = await async_client.chat.create_completion()
        assert chat is None

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_completion_with_all_params(self, async_client: AsyncScholarai) -> None:
        chat = await async_client.chat.create_completion(
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            model="model",
            stream=True,
        )
        assert chat is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_completion(self, async_client: AsyncScholarai) -> None:
        response = await async_client.chat.with_raw_response.create_completion()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert chat is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_completion(self, async_client: AsyncScholarai) -> None:
        async with async_client.chat.with_streaming_response.create_completion() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert chat is None

        assert cast(Any, response.is_closed) is True
