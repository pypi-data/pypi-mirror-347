# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from contextual import ContextualAI, AsyncContextualAI
from tests.utils import assert_matches_type
from contextual.types.agents.evaluate import EvaluationJobMetadata, ListEvaluationJobsResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestJobs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: ContextualAI) -> None:
        job = client.agents.evaluate.jobs.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ListEvaluationJobsResponse, job, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: ContextualAI) -> None:
        response = client.agents.evaluate.jobs.with_raw_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(ListEvaluationJobsResponse, job, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: ContextualAI) -> None:
        with client.agents.evaluate.jobs.with_streaming_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(ListEvaluationJobsResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: ContextualAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.agents.evaluate.jobs.with_raw_response.list(
                "",
            )

    @parametrize
    def test_method_cancel(self, client: ContextualAI) -> None:
        job = client.agents.evaluate.jobs.cancel(
            job_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            agent_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, job, path=["response"])

    @parametrize
    def test_raw_response_cancel(self, client: ContextualAI) -> None:
        response = client.agents.evaluate.jobs.with_raw_response.cancel(
            job_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            agent_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(object, job, path=["response"])

    @parametrize
    def test_streaming_response_cancel(self, client: ContextualAI) -> None:
        with client.agents.evaluate.jobs.with_streaming_response.cancel(
            job_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            agent_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(object, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_cancel(self, client: ContextualAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.agents.evaluate.jobs.with_raw_response.cancel(
                job_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                agent_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            client.agents.evaluate.jobs.with_raw_response.cancel(
                job_id="",
                agent_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

    @parametrize
    def test_method_metadata(self, client: ContextualAI) -> None:
        job = client.agents.evaluate.jobs.metadata(
            job_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            agent_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(EvaluationJobMetadata, job, path=["response"])

    @parametrize
    def test_raw_response_metadata(self, client: ContextualAI) -> None:
        response = client.agents.evaluate.jobs.with_raw_response.metadata(
            job_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            agent_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(EvaluationJobMetadata, job, path=["response"])

    @parametrize
    def test_streaming_response_metadata(self, client: ContextualAI) -> None:
        with client.agents.evaluate.jobs.with_streaming_response.metadata(
            job_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            agent_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(EvaluationJobMetadata, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_metadata(self, client: ContextualAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.agents.evaluate.jobs.with_raw_response.metadata(
                job_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                agent_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            client.agents.evaluate.jobs.with_raw_response.metadata(
                job_id="",
                agent_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )


class TestAsyncJobs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncContextualAI) -> None:
        job = await async_client.agents.evaluate.jobs.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ListEvaluationJobsResponse, job, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncContextualAI) -> None:
        response = await async_client.agents.evaluate.jobs.with_raw_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(ListEvaluationJobsResponse, job, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncContextualAI) -> None:
        async with async_client.agents.evaluate.jobs.with_streaming_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(ListEvaluationJobsResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncContextualAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.agents.evaluate.jobs.with_raw_response.list(
                "",
            )

    @parametrize
    async def test_method_cancel(self, async_client: AsyncContextualAI) -> None:
        job = await async_client.agents.evaluate.jobs.cancel(
            job_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            agent_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, job, path=["response"])

    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncContextualAI) -> None:
        response = await async_client.agents.evaluate.jobs.with_raw_response.cancel(
            job_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            agent_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(object, job, path=["response"])

    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncContextualAI) -> None:
        async with async_client.agents.evaluate.jobs.with_streaming_response.cancel(
            job_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            agent_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(object, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncContextualAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.agents.evaluate.jobs.with_raw_response.cancel(
                job_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                agent_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            await async_client.agents.evaluate.jobs.with_raw_response.cancel(
                job_id="",
                agent_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

    @parametrize
    async def test_method_metadata(self, async_client: AsyncContextualAI) -> None:
        job = await async_client.agents.evaluate.jobs.metadata(
            job_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            agent_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(EvaluationJobMetadata, job, path=["response"])

    @parametrize
    async def test_raw_response_metadata(self, async_client: AsyncContextualAI) -> None:
        response = await async_client.agents.evaluate.jobs.with_raw_response.metadata(
            job_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            agent_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(EvaluationJobMetadata, job, path=["response"])

    @parametrize
    async def test_streaming_response_metadata(self, async_client: AsyncContextualAI) -> None:
        async with async_client.agents.evaluate.jobs.with_streaming_response.metadata(
            job_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            agent_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(EvaluationJobMetadata, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_metadata(self, async_client: AsyncContextualAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.agents.evaluate.jobs.with_raw_response.metadata(
                job_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                agent_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            await async_client.agents.evaluate.jobs.with_raw_response.metadata(
                job_id="",
                agent_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )
