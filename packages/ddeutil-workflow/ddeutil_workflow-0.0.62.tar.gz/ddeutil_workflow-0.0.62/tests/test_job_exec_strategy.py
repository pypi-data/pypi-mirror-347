from concurrent.futures import Future, ThreadPoolExecutor
from threading import Event

import pytest
from ddeutil.workflow.exceptions import JobException
from ddeutil.workflow.job import Job, local_execute_strategy
from ddeutil.workflow.result import CANCEL, FAILED, SUCCESS, Result
from ddeutil.workflow.workflow import Workflow


def test_job_exec_strategy():
    job: Job = Workflow.from_conf(name="wf-run-python-raise-for-job").job(
        "job-complete"
    )
    rs = local_execute_strategy(job, {"sleep": "0.1"}, {})
    assert rs.status == SUCCESS
    assert rs.context == {
        "9873503202": {
            "matrix": {"sleep": "0.1"},
            "stages": {"success": {"outputs": {"result": "success"}}},
        },
    }


def test_job_exec_strategy_skip_stage():
    job: Job = Workflow.from_conf(name="wf-run-python-raise-for-job").job(
        "job-stage-condition"
    )
    rs = local_execute_strategy(job, {"sleep": "1"}, {})
    assert rs.status == SUCCESS
    assert rs.context == {
        "2150810470": {
            "matrix": {"sleep": "1"},
            "stages": {
                "equal-one": {"outputs": {"result": "pass-condition"}},
                "not-equal-one": {"outputs": {}, "skipped": True},
            },
        },
    }


def test_job_exec_strategy_catch_stage_error():
    job: Job = Workflow.from_conf(
        "wf-run-python-raise-for-job",
        extras={"stage_raise_error": False},
    ).job("final-job")

    rs = Result()
    with pytest.raises(JobException):
        local_execute_strategy(job, {"name": "foo"}, {}, result=rs)

    assert rs.status == FAILED
    assert rs.context == {
        "5027535057": {
            "matrix": {"name": "foo"},
            "stages": {
                "1772094681": {"outputs": {}},
                "raise-error": {
                    "outputs": {},
                    "errors": {
                        "name": "ValueError",
                        "message": "Testing raise error inside PyStage!!!",
                    },
                },
            },
            "errors": {
                "name": "JobException",
                "message": (
                    "Strategy break because stage, 'raise-error', return "
                    "`FAILED` status."
                ),
            },
        },
    }


def test_job_exec_strategy_catch_job_error():
    job: Job = Workflow.from_conf(
        "wf-run-python-raise-for-job",
        extras={"stage_raise_error": True},
    ).job("final-job")
    rs = Result()
    with pytest.raises(JobException):
        local_execute_strategy(job, {"name": "foo"}, {}, result=rs)

    assert rs.status == FAILED
    assert rs.context == {
        "5027535057": {
            "matrix": {"name": "foo"},
            "stages": {"1772094681": {"outputs": {}}},
            "errors": {
                "name": "StageException",
                "message": (
                    "PyStage: ValueError: Testing raise error inside PyStage!!!"
                ),
            },
        },
    }


def test_job_exec_strategy_event_set():
    job: Job = Workflow.from_conf(name="wf-run-python-raise-for-job").job(
        "second-job"
    )
    event = Event()
    rs = Result()
    with ThreadPoolExecutor(max_workers=1) as executor:
        future: Future = executor.submit(
            local_execute_strategy, job, {}, {}, result=rs, event=event
        )
        event.set()

    with pytest.raises(JobException):
        future.result()

    assert rs.status == CANCEL
    assert rs.context["EMPTY"]["errors"] == {
        "name": "JobException",
        "message": "Job strategy was canceled because event was set.",
    }


def test_job_exec_strategy_raise():
    job: Job = Workflow.from_conf(name="wf-run-python-raise-for-job").job(
        "first-job"
    )
    rs = Result()
    with pytest.raises(JobException):
        local_execute_strategy(job, {}, {}, result=rs)

    assert rs.status == FAILED
    assert rs.context == {
        "EMPTY": {
            "matrix": {},
            "stages": {},
            "errors": {
                "name": "StageException",
                "message": (
                    "PyStage: ValueError: Testing raise error inside PyStage!!!"
                ),
            },
        },
    }
