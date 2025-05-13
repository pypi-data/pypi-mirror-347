from datetime import datetime, timedelta
from unittest import mock

import pytest
from ddeutil.workflow import SUCCESS, Config, Result, WorkflowPoke
from ddeutil.workflow.exceptions import WorkflowException

from .utils import dump_yaml_context


@pytest.mark.poke
def test_workflow_poke(test_path):
    workflow = WorkflowPoke.model_validate(
        obj={
            "extras": {"enable_write_audit": False, "enable_write_log": True},
            "name": "tmp-wf-scheduling-minute",
            "on": [{"cronjob": "* * * * *", "timezone": "Asia/Bangkok"}],
            "params": {"run-dt": "datetime"},
            "jobs": {
                "first-job": {
                    "stages": [
                        {"name": "Empty stage"},
                        {
                            "name": "Hello stage",
                            "echo": "Hello ${{ params.run-dt | fmt('%Y-%m-%d') }}",
                        },
                    ]
                }
            },
        }
    )
    result: Result = workflow.poke(
        params={"run-dt": datetime(2024, 1, 1)},
    )

    # FIXME: The result that return from this test is random between 1 and 2
    # NOTE: Respec the result from poking should have only 1 result.
    # assert len(result.context["outputs"]) == 1
    assert isinstance(result.context["outputs"][0], Result)
    assert result.context["outputs"][0].status == 0
    assert result.context["outputs"][0].context == {
        "params": {"run-dt": datetime(2024, 1, 1)},
        "release": {
            "type": "poking",
            "logical_date": result.context["outputs"][0].context["release"][
                "logical_date"
            ],
        },
        "jobs": {
            "first-job": {
                "stages": {
                    "6708019737": {"outputs": {}},
                    "9818133124": {"outputs": {}},
                },
            },
        },
    }

    # NOTE: Respec the run_id does not equal to the parent_run_id.
    assert (
        result.context["outputs"][0].run_id
        == result.context["outputs"][0].parent_run_id
    )

    # NOTE: Raise because start date gather than the current date.
    with pytest.raises(WorkflowException):
        workflow.poke(start_date=datetime.now() + timedelta(days=1))


@pytest.mark.poke
@mock.patch.object(Config, "enable_write_audit", False)
def test_workflow_poke_no_queue(test_path):
    with dump_yaml_context(
        test_path / "conf/demo/01_99_wf_test_wf_poke_no_schedule.yml",
        data="""
        tmp-wf-scheduling-daily:
          type: WorkflowPoke
          on:
            - cronjob: "30 3 * * *"
              timezone: "Asia/Bangkok"
          jobs:
            do-nothing:
              stages:
                - name: "Empty stage"
        """,
    ):
        workflow = WorkflowPoke.from_conf(name="tmp-wf-scheduling-daily")

        # NOTE: Poking with the current datetime.
        rs: Result = workflow.poke(params={"asat-dt": datetime(2024, 1, 1)})
        assert rs.status == SUCCESS
        assert rs.context == {"outputs": []}


@pytest.mark.poke
def test_workflow_poke_raise():
    workflow = WorkflowPoke(name="tmp-wf-scheduling-common")

    # Raise: If a period value is lower than 0.
    with pytest.raises(WorkflowException):
        workflow.poke(periods=0)

    # Raise: If a period value is lower than 0.
    with pytest.raises(WorkflowException):
        workflow.poke(periods=-5)


@pytest.mark.poke
def test_workflow_poke_with_start_date_and_period(test_path):
    with dump_yaml_context(
        test_path / "conf/demo/01_99_wf_test_wf_poke_with_start_date.yml",
        data="""
        tmp-wf-scheduling-with-name:
          type: WorkflowPoke
          on:
            - 'every_minute_bkk'
          params: {name: str}
          jobs:
            first-job:
              stages:
                - name: "Hello stage"
                  echo: "Hello ${{ params.name | title }}"
        """,
    ):
        workflow = WorkflowPoke.from_conf(
            name="tmp-wf-scheduling-with-name",
            extras={"enable_write_audit": False},
        )

        # NOTE: Poking with specific start datetime.
        result: Result = workflow.poke(
            start_date=datetime(2024, 1, 1, 0, 0, 15),
            periods=2,
            params={"name": "FOO"},
        )
        assert len(result.context["outputs"]) == 2
        outputs: list[Result] = result.context["outputs"]
        assert outputs[0].parent_run_id != outputs[1].parent_run_id
        assert outputs[0].context["release"]["logical_date"] == datetime(
            2024, 1, 1, 0, 1
        )
        assert outputs[1].context["release"]["logical_date"] == datetime(
            2024, 1, 1, 0, 2
        )


@pytest.mark.poke
def test_workflow_poke_no_event():
    workflow = WorkflowPoke.model_validate(
        {
            "name": "tmp-wf-poke-no-on",
            "params": {"name": "str"},
            "jobs": {
                "first-job": {
                    "stages": [
                        {
                            "name": "Echo Stage",
                            "echo": "Hello ${{ params.name }}",
                        },
                    ],
                },
            },
            "extras": {"enable_write_audit": False},
        }
    )
    rs: Result = workflow.poke(params={"name": "FOO"})
    assert rs.status == SUCCESS
    assert rs.context == {"outputs": []}
