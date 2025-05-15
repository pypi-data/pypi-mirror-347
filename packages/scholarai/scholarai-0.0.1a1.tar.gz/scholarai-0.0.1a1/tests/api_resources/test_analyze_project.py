# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scholarai import Scholarai, AsyncScholarai
from tests.utils import assert_matches_type
from scholarai.types import AnalyzeProjectBatchAnalyzeResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAnalyzeProject:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_batch_analyze(self, client: Scholarai) -> None:
        analyze_project = client.analyze_project.batch_analyze(
            analysis_mode="analysis_mode",
            project_name="project_name",
            question=["string"],
        )
        assert_matches_type(AnalyzeProjectBatchAnalyzeResponse, analyze_project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_batch_analyze(self, client: Scholarai) -> None:
        response = client.analyze_project.with_raw_response.batch_analyze(
            analysis_mode="analysis_mode",
            project_name="project_name",
            question=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        analyze_project = response.parse()
        assert_matches_type(AnalyzeProjectBatchAnalyzeResponse, analyze_project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_batch_analyze(self, client: Scholarai) -> None:
        with client.analyze_project.with_streaming_response.batch_analyze(
            analysis_mode="analysis_mode",
            project_name="project_name",
            question=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            analyze_project = response.parse()
            assert_matches_type(AnalyzeProjectBatchAnalyzeResponse, analyze_project, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAnalyzeProject:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_batch_analyze(self, async_client: AsyncScholarai) -> None:
        analyze_project = await async_client.analyze_project.batch_analyze(
            analysis_mode="analysis_mode",
            project_name="project_name",
            question=["string"],
        )
        assert_matches_type(AnalyzeProjectBatchAnalyzeResponse, analyze_project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_batch_analyze(self, async_client: AsyncScholarai) -> None:
        response = await async_client.analyze_project.with_raw_response.batch_analyze(
            analysis_mode="analysis_mode",
            project_name="project_name",
            question=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        analyze_project = await response.parse()
        assert_matches_type(AnalyzeProjectBatchAnalyzeResponse, analyze_project, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_batch_analyze(self, async_client: AsyncScholarai) -> None:
        async with async_client.analyze_project.with_streaming_response.batch_analyze(
            analysis_mode="analysis_mode",
            project_name="project_name",
            question=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            analyze_project = await response.parse()
            assert_matches_type(AnalyzeProjectBatchAnalyzeResponse, analyze_project, path=["response"])

        assert cast(Any, response.is_closed) is True
