import asyncio
import os
import time

import pytest
from futurehouse_client.clients import (
    JobNames,
    PQATaskResponse,
    TaskResponseVerbose,
)
from futurehouse_client.clients.rest_client import RestClient, TaskFetchError
from futurehouse_client.models.app import Stage, TaskRequest
from futurehouse_client.models.rest import ExecutionStatus
from pytest_subtests import SubTests

ADMIN_API_KEY = os.environ["PLAYWRIGHT_ADMIN_API_KEY"]
PUBLIC_API_KEY = os.environ["PLAYWRIGHT_PUBLIC_API_KEY"]
TEST_MAX_POLLS = 100


@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
def test_futurehouse_dummy_env_crow():
    client = RestClient(
        stage=Stage.DEV,
        api_key=ADMIN_API_KEY,
    )

    task_data = TaskRequest(
        name=JobNames.from_string("dummy"),
        query="How many moons does earth have?",
    )
    client.create_task(task_data)

    while (task_status := client.get_task().status) in {"queued", "in progress"}:
        time.sleep(5)

    assert task_status == "success"


def test_insufficient_permissions_request():
    # Create a new instance so that cached credentials aren't reused
    client = RestClient(
        stage=Stage.DEV,
        api_key=PUBLIC_API_KEY,
    )
    task_data = TaskRequest(
        name=JobNames.from_string("dummy"),
        query="How many moons does earth have?",
    )

    with pytest.raises(TaskFetchError) as exc_info:
        client.create_task(task_data)

    assert "Error creating task" in str(exc_info.value)


@pytest.mark.timeout(300)
@pytest.mark.asyncio
async def test_job_response(subtests: SubTests):  # noqa: PLR0915
    client = RestClient(
        stage=Stage.DEV,
        api_key=ADMIN_API_KEY,
    )
    task_data = TaskRequest(
        name=JobNames.from_string("crow"),
        query="How many moons does earth have?",
    )
    task_id = client.create_task(task_data)
    atask_id = await client.acreate_task(task_data)

    with subtests.test("Test TaskResponse with queued task"):
        task_response = client.get_task(task_id)
        assert task_response.status in {"queued", "in progress"}
        assert task_response.job_name == task_data.name
        assert task_response.query == task_data.query
        task_response = await client.aget_task(atask_id)
        assert task_response.status in {"queued", "in progress"}
        assert task_response.job_name == task_data.name
        assert task_response.query == task_data.query

    for _ in range(TEST_MAX_POLLS):
        task_response = client.get_task(task_id)
        if task_response.status in ExecutionStatus.terminal_states():
            break
        await asyncio.sleep(5)

    for _ in range(TEST_MAX_POLLS):
        task_response = await client.aget_task(atask_id)
        if task_response.status in ExecutionStatus.terminal_states():
            break
        await asyncio.sleep(5)

    with subtests.test("Test PQA job response"):
        task_response = client.get_task(task_id)
        assert isinstance(task_response, PQATaskResponse)
        # assert it has general fields
        assert task_response.status == "success"
        assert task_response.task_id is not None
        assert task_data.name in task_response.job_name
        assert task_data.query in task_response.query
        # assert it has PQA specific fields
        assert task_response.answer is not None
        # assert it's not verbose
        assert not hasattr(task_response, "environment_frame")
        assert not hasattr(task_response, "agent_state")

    with subtests.test("Test async PQA job response"):
        task_response = await client.aget_task(atask_id)
        assert isinstance(task_response, PQATaskResponse)
        # assert it has general fields
        assert task_response.status == "success"
        assert task_response.task_id is not None
        assert task_data.name in task_response.job_name
        assert task_data.query in task_response.query
        # assert it has PQA specific fields
        assert task_response.answer is not None
        # assert it's not verbose
        assert not hasattr(task_response, "environment_frame")
        assert not hasattr(task_response, "agent_state")

    with subtests.test("Test task response with verbose"):
        task_response = client.get_task(task_id, verbose=True)
        assert isinstance(task_response, TaskResponseVerbose)
        assert task_response.status == "success"
        assert task_response.environment_frame is not None
        assert task_response.agent_state is not None

    with subtests.test("Test task async response with verbose"):
        task_response = await client.aget_task(atask_id, verbose=True)
        assert isinstance(task_response, TaskResponseVerbose)
        assert task_response.status == "success"
        assert task_response.environment_frame is not None
        assert task_response.agent_state is not None


@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
def test_run_until_done_futurehouse_dummy_env_crow():
    client = RestClient(
        stage=Stage.DEV,
        api_key=ADMIN_API_KEY,
    )

    task_data = TaskRequest(
        name=JobNames.from_string("dummy"),
        query="How many moons does earth have?",
    )

    tasks_to_do = [task_data, task_data]

    results = client.run_tasks_until_done(tasks_to_do)

    assert len(results) == len(tasks_to_do), "Should return 2 tasks."
    assert all(task.status == "success" for task in results)


@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
@pytest.mark.asyncio
async def test_arun_until_done_futurehouse_dummy_env_crow():
    client = RestClient(
        stage=Stage.DEV,
        api_key=ADMIN_API_KEY,
    )

    task_data = TaskRequest(
        name=JobNames.from_string("dummy"),
        query="How many moons does earth have?",
    )

    tasks_to_do = [task_data, task_data]

    results = await client.arun_tasks_until_done(tasks_to_do)

    assert len(results) == len(tasks_to_do), "Should return 2 tasks."
    assert all(task.status == "success" for task in results)


@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
@pytest.mark.asyncio
async def test_timeout_run_until_done_futurehouse_dummy_env_crow():
    client = RestClient(
        stage=Stage.DEV,
        api_key=ADMIN_API_KEY,
    )

    task_data = TaskRequest(
        name=JobNames.from_string("dummy"),
        query="How many moons does earth have?",
    )

    tasks_to_do = [task_data, task_data]

    results = await client.arun_tasks_until_done(
        tasks_to_do, verbose=True, timeout=5, progress_bar=True
    )

    assert len(results) == len(tasks_to_do), "Should return 2 tasks."
    assert all(task.status != "success" for task in results), "Should not be success."
    assert all(not isinstance(task, PQATaskResponse) for task in results), (
        "Should be verbose."
    )

    results = client.run_tasks_until_done(
        tasks_to_do, verbose=True, timeout=5, progress_bar=True
    )

    assert len(results) == len(tasks_to_do), "Should return 2 tasks."
    assert all(task.status != "success" for task in results), "Should not be success."
    assert all(not isinstance(task, PQATaskResponse) for task in results), (
        "Should be verbose."
    )
