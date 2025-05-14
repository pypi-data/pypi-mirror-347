import shutil
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime
from textwrap import dedent
from threading import Event
from unittest import mock

from ddeutil.core import getdot
from ddeutil.workflow import (
    FAILED,
    SUCCESS,
    Config,
    Job,
    Result,
    Workflow,
    extract_call,
)

from .utils import dump_yaml_context


def test_workflow_exec():
    job: Job = Job(
        stages=[{"name": "Sleep", "run": "import time\ntime.sleep(2)"}],
    )
    workflow: Workflow = Workflow(
        name="demo-workflow", jobs={"sleep-run": job, "sleep-again-run": job}
    )
    rs: Result = workflow.execute(params={}, max_job_parallel=1)
    assert rs.status == 0
    assert rs.context == {
        "params": {},
        "jobs": {
            "sleep-again-run": {
                "stages": {"7972360640": {"outputs": {}}},
            },
        },
    }


def test_workflow_exec_timeout():
    job: Job = Job(
        stages=[
            {"name": "Sleep", "run": "import time\ntime.sleep(2)"},
            {"name": "Echo Last Stage", "echo": "the last stage"},
        ],
    )
    workflow: Workflow = Workflow(
        name="demo-workflow",
        jobs={"sleep-run": job, "sleep-again-run": job},
    )
    rs: Result = workflow.execute(params={}, timeout=1.25, max_job_parallel=1)
    assert rs.status == FAILED
    assert rs.context == {
        "errors": {
            "name": "WorkflowException",
            "message": "'demo-workflow' was timeout.",
        },
        "params": {},
        "jobs": {
            "sleep-again-run": {
                "stages": {"7972360640": {"outputs": {}}},
                "errors": {
                    "name": "JobException",
                    "message": "Job strategy was canceled because event was set.",
                },
            },
        },
    }


def test_workflow_exec_raise_event_set():
    job: Job = Job(
        stages=[{"name": "Echo Last Stage", "echo": "the last stage"}],
    )
    workflow: Workflow = Workflow(
        name="demo-workflow",
        jobs={"sleep-run": job, "sleep-again-run": job},
    )
    event = Event()
    with ThreadPoolExecutor(max_workers=1) as executor:
        future: Future = executor.submit(
            workflow.execute,
            params={},
            timeout=1,
            event=event,
            max_job_parallel=1,
        )
        event.set()

    rs: Result = future.result()
    assert rs.status == FAILED
    assert rs.context == {
        "errors": {
            "name": "WorkflowException",
            "message": "Workflow job was canceled because event was set.",
        },
        "jobs": {},
        "params": {},
    }


def test_workflow_exec_py():
    workflow = Workflow.from_conf(name="wf-run-python")
    rs: Result = workflow.execute(
        params={
            "author-run": "Local Workflow",
            "run-date": "2024-01-01",
        },
    )
    assert rs.status == SUCCESS
    assert rs.context == {
        "params": {
            "author-run": "Local Workflow",
            "run-date": datetime(2024, 1, 1, 0, 0),
        },
        "jobs": {
            "first-job": {
                "stages": {
                    "printing": {"outputs": {"x": "Local Workflow"}},
                    "setting-x": {"outputs": {"x": 1}},
                },
            },
            "second-job": {
                "stages": {
                    "create-func": {
                        "outputs": {
                            "var_inside": "Create Function Inside",
                            "echo": "echo",
                        },
                    },
                    "call-func": {"outputs": {}},
                    "9150930869": {"outputs": {}},
                },
            },
            "final-job": {
                "stages": {
                    "1772094681": {
                        "outputs": {
                            "return_code": 0,
                            "stdout": "Hello World",
                            "stderr": None,
                        }
                    }
                },
            },
        },
    }


def test_workflow_exec_parallel():
    job: Job = Job(
        stages=[{"name": "Sleep", "run": "import time\ntime.sleep(2)"}],
    )
    workflow: Workflow = Workflow(
        name="demo-workflow", jobs={"sleep-run": job, "sleep-again-run": job}
    )
    rs: Result = workflow.execute(params={}, max_job_parallel=2)
    assert rs.status == SUCCESS
    assert rs.context == {
        "params": {},
        "jobs": {
            "sleep-again-run": {"stages": {"7972360640": {"outputs": {}}}},
        },
    }


def test_workflow_exec_parallel_timeout():
    job: Job = Job(
        stages=[
            {"name": "Sleep", "run": "import time\ntime.sleep(2)"},
            {"name": "Echo Last Stage", "echo": "the last stage"},
        ],
    )
    workflow: Workflow = Workflow(
        name="demo-workflow",
        jobs={
            "sleep-run": job,
            "sleep-again-run": job.model_copy(update={"needs": ["sleep-run"]}),
        },
        extras={"stage_default_id": False},
    )
    rs: Result = workflow.execute(params={}, timeout=1.25, max_job_parallel=2)
    assert rs.status == FAILED
    assert rs.context == {
        "params": {},
        "jobs": {
            "sleep-run": {
                "stages": {},
                "errors": {
                    "name": "JobException",
                    "message": "Job strategy was canceled because event was set.",
                },
            },
        },
        "errors": {
            "name": "WorkflowException",
            "message": "'demo-workflow' was timeout.",
        },
    }


def test_workflow_exec_py_with_parallel():
    workflow = Workflow.from_conf(name="wf-run-python")
    rs: Result = workflow.execute(
        params={
            "author-run": "Local Workflow",
            "run-date": "2024-01-01",
        },
        max_job_parallel=3,
    )
    assert rs.status == SUCCESS
    assert rs.context == {
        "params": {
            "author-run": "Local Workflow",
            "run-date": datetime(2024, 1, 1, 0, 0),
        },
        "jobs": {
            "first-job": {
                "stages": {
                    "printing": {"outputs": {"x": "Local Workflow"}},
                    "setting-x": {"outputs": {"x": 1}},
                },
            },
            "second-job": {
                "stages": {
                    "create-func": {
                        "outputs": {
                            "var_inside": "Create Function Inside",
                            "echo": "echo",
                        },
                    },
                    "call-func": {"outputs": {}},
                    "9150930869": {"outputs": {}},
                },
            },
            "final-job": {
                "stages": {
                    "1772094681": {
                        "outputs": {
                            "return_code": 0,
                            "stdout": "Hello World",
                            "stderr": None,
                        }
                    }
                },
            },
        },
    }


def test_workflow_exec_py_raise():
    rs: Result = Workflow.from_conf("wf-run-python-raise").execute(
        params={}, max_job_parallel=1
    )
    assert rs.status == FAILED
    assert rs.context == {
        "errors": {
            "name": "WorkflowException",
            "message": "Job, 'first-job', return `FAILED` status.",
        },
        "params": {},
        "jobs": {
            "first-job": {
                "errors": {
                    "name": "JobException",
                    "message": (
                        "Handler Error: StageException: PyStage: "
                        "ValueError: Testing raise error inside PyStage!!!"
                    ),
                },
                "stages": {},
            },
            "second-job": {"stages": {"1772094681": {"outputs": {}}}},
        },
    }


def test_workflow_exec_py_raise_parallel():
    rs: Result = Workflow.from_conf("wf-run-python-raise").execute(
        params={}, max_job_parallel=2
    )
    assert rs.status == FAILED
    assert rs.context == {
        "errors": {
            "name": "WorkflowException",
            "message": "Job, 'first-job', return `FAILED` status.",
        },
        "params": {},
        "jobs": {
            "first-job": {
                "errors": {
                    "name": "JobException",
                    "message": (
                        "Handler Error: StageException: PyStage: "
                        "ValueError: Testing raise error inside PyStage!!!"
                    ),
                },
                "stages": {},
            },
            "second-job": {"stages": {"1772094681": {"outputs": {}}}},
        },
    }


def test_workflow_exec_with_matrix():
    workflow: Workflow = Workflow.from_conf(name="wf-run-matrix")
    rs: Result = workflow.execute(params={"source": "src", "target": "tgt"})
    assert rs.status == SUCCESS
    assert rs.context == {
        "params": {"source": "src", "target": "tgt"},
        "jobs": {
            "multiple-system": {
                "strategies": {
                    "9696245497": {
                        "matrix": {
                            "table": "customer",
                            "system": "csv",
                            "partition": 2,
                        },
                        "stages": {
                            "customer-2": {"outputs": {"records": 1}},
                            "end-stage": {"outputs": {"passing_value": 10}},
                        },
                    },
                    "8141249744": {
                        "matrix": {
                            "table": "customer",
                            "system": "csv",
                            "partition": 3,
                        },
                        "stages": {
                            "customer-3": {"outputs": {"records": 1}},
                            "end-stage": {"outputs": {"passing_value": 10}},
                        },
                    },
                    "3590257855": {
                        "matrix": {
                            "table": "sales",
                            "system": "csv",
                            "partition": 1,
                        },
                        "stages": {
                            "sales-1": {"outputs": {"records": 1}},
                            "end-stage": {"outputs": {"passing_value": 10}},
                        },
                    },
                    "3698996074": {
                        "matrix": {
                            "table": "sales",
                            "system": "csv",
                            "partition": 2,
                        },
                        "stages": {
                            "sales-2": {"outputs": {"records": 1}},
                            "end-stage": {"outputs": {"passing_value": 10}},
                        },
                    },
                    "4390593385": {
                        "matrix": {
                            "table": "customer",
                            "system": "csv",
                            "partition": 4,
                        },
                        "stages": {
                            "customer-4": {"outputs": {"records": 1}},
                            "end-stage": {"outputs": {"passing_value": 10}},
                        },
                    },
                },
            },
        },
    }


def test_workflow_exec_needs():
    workflow = Workflow.from_conf(name="wf-run-depends")
    rs: Result = workflow.execute(params={"name": "bar"})
    assert rs.status == SUCCESS
    assert rs.context == {
        "params": {"name": "bar"},
        "jobs": {
            "final-job": {
                "stages": {
                    "8797330324": {
                        "outputs": {},
                    },
                },
            },
            "first-job": {
                "stages": {
                    "7824513474": {
                        "outputs": {},
                    },
                },
            },
            "second-job": {
                "stages": {
                    "1772094681": {
                        "outputs": {},
                    },
                },
            },
        },
    }


def test_workflow_exec_needs_condition():
    workflow = Workflow.from_conf(name="wf-run-depends-condition")
    rs: Result = workflow.execute(params={"name": "bar"})
    assert {
        "params": {"name": "bar"},
        "jobs": {
            "final-job": {
                "stages": {
                    "8797330324": {
                        "outputs": {},
                    },
                },
            },
            "first-job": {"skipped": True},
            "second-job": {"skipped": True},
        },
    } == rs.context


def test_workflow_exec_needs_parallel():
    workflow = Workflow.from_conf(name="wf-run-depends", extras={})
    rs: Result = workflow.execute(params={"name": "bar"}, max_job_parallel=3)
    assert {
        "params": {"name": "bar"},
        "jobs": {
            "final-job": {
                "stages": {
                    "8797330324": {
                        "outputs": {},
                    },
                },
            },
            "first-job": {
                "stages": {
                    "7824513474": {
                        "outputs": {},
                    },
                },
            },
            "second-job": {
                "stages": {
                    "1772094681": {
                        "outputs": {},
                    },
                },
            },
        },
    } == rs.context


def test_workflow_exec_call(test_path):
    with dump_yaml_context(
        test_path / "conf/demo/01_99_wf_test_wf_call_csv_to_parquet.yml",
        data="""
        tmp-wf-call-csv-to-parquet:
          type: Workflow
          params:
            run-date: datetime
            source: str
            sink: str
          jobs:
            extract-load:
              stages:
                - name: "Extract & Load Local System"
                  id: extract-load
                  uses: tasks/el-csv-to-parquet@polars-dir
                  with:
                    source: ${{ params.source }}
                    sink: ${{ params.sink }}
        """,
    ):
        workflow = Workflow.from_conf(name="tmp-wf-call-csv-to-parquet")
        rs: Result = workflow.execute(
            params={
                "run-date": datetime(2024, 1, 1),
                "source": "ds_csv_local_file",
                "sink": "ds_parquet_local_file_dir",
            },
        )
        assert rs.status == SUCCESS
        assert rs.context == {
            "params": {
                "run-date": datetime(2024, 1, 1),
                "source": "ds_csv_local_file",
                "sink": "ds_parquet_local_file_dir",
            },
            "jobs": {
                "extract-load": {
                    "stages": {
                        "extract-load": {
                            "outputs": {"records": 1},
                        },
                    },
                },
            },
        }


def test_workflow_exec_call_override_registry(test_path):
    task_path = test_path.parent / "mock_tests"
    task_path.mkdir(exist_ok=True)
    (task_path / "__init__.py").open(mode="w")
    (task_path / "mock_tasks").mkdir(exist_ok=True)

    with (task_path / "mock_tasks/__init__.py").open(mode="w") as f:
        f.write(
            dedent(
                """
            from ddeutil.workflow import tag, Result

            @tag("v1", alias="get-info")
            def get_info(result: Result):
                result.trace.info("... [CALLER]: Info from mock tasks")
                return {"get-info": "success"}
            """.strip(
                    "\n"
                )
            )
        )

    with dump_yaml_context(
        test_path / "conf/demo/01_99_wf_test_wf_exec_call_override.yml",
        data="""
        tmp-wf-exec-call-override:
          type: Workflow
          jobs:
            first-job:
              stages:
                - name: "Call from mock tasks"
                  uses: mock_tasks/get-info@v1
        """,
    ):
        func = extract_call("mock_tasks/get-info@v1", registries=["mock_tests"])
        assert func().name == "get-info"

        workflow = Workflow.from_conf(
            name="tmp-wf-exec-call-override",
            extras={"registry_caller": ["mock_tests"]},
        )
        rs: Result = workflow.execute(params={})
        assert rs.status == SUCCESS
        assert rs.context == {
            "params": {},
            "jobs": {
                "first-job": {
                    "stages": {
                        "4030788970": {"outputs": {"get-info": "success"}}
                    },
                },
            },
        }

    shutil.rmtree(task_path)


def test_workflow_exec_call_with_prefix(test_path):
    with dump_yaml_context(
        test_path / "conf/demo/01_99_wf_test_wf_call_mssql_proc.yml",
        data="""
        tmp-wf-call-mssql-proc:
          type: Workflow
          params:
            run_date: datetime
            sp_name: str
            source_name: str
            target_name: str
          jobs:
            transform:
              stages:
                - name: "Transform Data in MS SQL Server"
                  id: transform
                  uses: tasks/mssql-proc@odbc
                  with:
                    exec: ${{ params.sp_name }}
                    params:
                      run_mode: "T"
                      run_date: ${{ params.run_date }}
                      source: ${{ params.source_name }}
                      target: ${{ params.target_name }}
        """,
    ):
        workflow = Workflow.from_conf(name="tmp-wf-call-mssql-proc")
        rs = workflow.execute(
            params={
                "run_date": datetime(2024, 1, 1),
                "sp_name": "proc-name",
                "source_name": "src",
                "target_name": "tgt",
            },
        )
        assert rs.status == SUCCESS
        assert rs.context == {
            "params": {
                "run_date": datetime(2024, 1, 1),
                "sp_name": "proc-name",
                "source_name": "src",
                "target_name": "tgt",
            },
            "jobs": {
                "transform": {
                    "stages": {
                        "transform": {
                            "outputs": {
                                "exec": "proc-name",
                                "params": {
                                    "run_mode": "T",
                                    "run_date": datetime(2024, 1, 1),
                                    "source": "src",
                                    "target": "tgt",
                                },
                            },
                        },
                    },
                },
            },
        }


def test_workflow_exec_trigger():
    workflow = Workflow.from_conf(name="wf-trigger", extras={})
    job = workflow.job("trigger-job")
    rs = job.set_outputs(job.execute(params={}).context, to={})
    assert {
        "author-run": "Trigger Runner",
        "run-date": datetime(2024, 8, 1),
    } == getdot("jobs.trigger-job.stages.trigger-stage.outputs.params", rs)


def test_workflow_exec_foreach(test_path):
    with dump_yaml_context(
        test_path / "conf/demo/01_99_wf_test_wf_foreach.yml",
        data="""
        tmp-wf-foreach:
          type: Workflow
          jobs:
            transform:
              stages:
                - name: "Get Items before run foreach"
                  id: get-items
                  uses: tasks/get-items@demo
                - name: "Create variable"
                  id: create-variable
                  run: |
                    foo: str = "bar"
                - name: "For-each item"
                  id: foreach-stage
                  foreach: ${{ stages.get-items.outputs.items }}
                  stages:
                    - name: "Echo stage"
                      echo: |
                        Start run with item ${{ item }}
                        Import variable ${{ stages.create-variable.outputs.foo }}
                    - name: "Final Echo"
                      if: ${{ item }} == 4
                      echo: |
                        Final run
        """,
    ):
        workflow = Workflow.from_conf(name="tmp-wf-foreach")
        rs = workflow.execute(params={})
        assert rs.status == SUCCESS
        assert rs.context == {
            "params": {},
            "jobs": {
                "transform": {
                    "stages": {
                        "get-items": {"outputs": {"items": [1, 2, 3, 4]}},
                        "create-variable": {"outputs": {"foo": "bar"}},
                        "foreach-stage": {
                            "outputs": {
                                "items": [1, 2, 3, 4],
                                "foreach": {
                                    1: {
                                        "item": 1,
                                        "stages": {
                                            "2709471980": {"outputs": {}},
                                            "9263488742": {
                                                "outputs": {},
                                                "skipped": True,
                                            },
                                        },
                                    },
                                    2: {
                                        "item": 2,
                                        "stages": {
                                            "2709471980": {"outputs": {}},
                                            "9263488742": {
                                                "outputs": {},
                                                "skipped": True,
                                            },
                                        },
                                    },
                                    3: {
                                        "item": 3,
                                        "stages": {
                                            "2709471980": {"outputs": {}},
                                            "9263488742": {
                                                "outputs": {},
                                                "skipped": True,
                                            },
                                        },
                                    },
                                    4: {
                                        "item": 4,
                                        "stages": {
                                            "2709471980": {"outputs": {}},
                                            "9263488742": {"outputs": {}},
                                        },
                                    },
                                },
                            }
                        },
                    }
                }
            },
        }


def test_workflow_exec_foreach_get_inside(test_path):
    with dump_yaml_context(
        test_path / "conf/demo/01_99_wf_test_wf_foreach_get_inside.yml",
        data="""
        tmp-wf-foreach-inside:
          type: Workflow
          jobs:
            transform:
              stages:
                - name: "Get Items before run foreach"
                  id: get-items
                  uses: tasks/get-items@demo
                - name: "Create variable"
                  id: create-variable
                  run: |
                    foo: str = "bar"
                - name: "For-each item"
                  id: foreach-stage
                  foreach: ${{ stages.get-items.outputs.items }}
                  stages:
                    - name: "Echo stage"
                      id: prepare-variable
                      run: |
                        foo: str = 'baz${{ item }}'
                    - name: "Final Echo"
                      if: ${{ item }} == 4
                      echo: |
                        This is the final foo, it be: ${{ stages.prepare-variable.outputs.foo }}
        """,
    ):
        workflow = Workflow.from_conf(name="tmp-wf-foreach-inside")
        rs = workflow.execute(params={})
        assert rs.status == SUCCESS
        assert rs.context == {
            "params": {},
            "jobs": {
                "transform": {
                    "stages": {
                        "get-items": {"outputs": {"items": [1, 2, 3, 4]}},
                        "create-variable": {"outputs": {"foo": "bar"}},
                        "foreach-stage": {
                            "outputs": {
                                "items": [1, 2, 3, 4],
                                "foreach": {
                                    1: {
                                        "item": 1,
                                        "stages": {
                                            "prepare-variable": {
                                                "outputs": {"foo": "baz1"}
                                            },
                                            "9263488742": {
                                                "outputs": {},
                                                "skipped": True,
                                            },
                                        },
                                    },
                                    2: {
                                        "item": 2,
                                        "stages": {
                                            "prepare-variable": {
                                                "outputs": {"foo": "baz2"}
                                            },
                                            "9263488742": {
                                                "outputs": {},
                                                "skipped": True,
                                            },
                                        },
                                    },
                                    3: {
                                        "item": 3,
                                        "stages": {
                                            "prepare-variable": {
                                                "outputs": {"foo": "baz3"}
                                            },
                                            "9263488742": {
                                                "outputs": {},
                                                "skipped": True,
                                            },
                                        },
                                    },
                                    4: {
                                        "item": 4,
                                        "stages": {
                                            "prepare-variable": {
                                                "outputs": {"foo": "baz4"}
                                            },
                                            "9263488742": {"outputs": {}},
                                        },
                                    },
                                },
                            }
                        },
                    }
                }
            },
        }


@mock.patch.object(Config, "stage_raise_error", False)
def test_workflow_exec_raise_param(test_path):
    with dump_yaml_context(
        test_path / "conf/demo/01_99_wf_test_wf_exec_raise_param.yml",
        data="""
        tmp-wf-exec-raise-param:
          type: Workflow
          params:
            name:
              desc: "A name parameter of this workflow."
              type: str
          jobs:
            start-job:
              stages:
                - name: "Get param that not set"
                  id: get-param
                  echo: "Passing name ${{ params.name }}"

                - name: "Call after above stage raise"
                  id: check
                  echo: "Hello after Raise Error"
        """,
    ):
        rs: Result = Workflow.from_conf(
            "tmp-wf-exec-raise-param",
            extras={"stage_raise_error": False},
        ).execute(params={"stream": "demo-stream"}, max_job_parallel=1)
        assert rs.status == FAILED
        assert rs.context == {
            "params": {"stream": "demo-stream"},
            "jobs": {
                "start-job": {
                    "stages": {
                        "get-param": {
                            "outputs": {},
                            "errors": {
                                "name": "UtilException",
                                "message": (
                                    "Parameters does not get dot with caller: "
                                    "'params.name'."
                                ),
                            },
                        }
                    },
                    "errors": {
                        "name": "JobException",
                        "message": (
                            "Strategy break because stage, 'get-param', "
                            "return `FAILED` status."
                        ),
                    },
                }
            },
            "errors": {
                "message": "Job, 'start-job', return `FAILED` status.",
                "name": "WorkflowException",
            },
        }


@mock.patch.object(Config, "stage_raise_error", False)
def test_workflow_exec_raise_job_trigger(test_path):
    with dump_yaml_context(
        test_path / "conf/demo/01_99_wf_test_wf_exec_raise_job_trigger.yml",
        data="""
        tmp-wf-exec-raise-job-trigger:
          type: Workflow
          params:
            name:
              desc: "A name parameter of this workflow."
              type: str
          jobs:
            final-job:
              needs: [ "start-job" ]
              stages:
                - name: "Call after above stage raise"
                  id: check
                  echo: "Hello after Raise Error"
            start-job:
              stages:
                - name: "Get param that not set"
                  id: get-param
                  echo: "Passing name ${{ params.name }}"

        """,
    ):
        workflow = Workflow.from_conf(name="tmp-wf-exec-raise-job-trigger")
        rs: Result = workflow.execute(
            params={"stream": "demo-stream"}, max_job_parallel=1
        )
        assert rs.status == FAILED
        assert rs.context == {
            "params": {"stream": "demo-stream"},
            "jobs": {
                "start-job": {
                    "stages": {
                        "get-param": {
                            "outputs": {},
                            "errors": {
                                "name": "UtilException",
                                "message": (
                                    "Parameters does not get dot with caller: "
                                    "'params.name'."
                                ),
                            },
                        },
                    },
                    "errors": {
                        "name": "JobException",
                        "message": (
                            "Strategy break because stage, 'get-param', "
                            "return `FAILED` status."
                        ),
                    },
                },
            },
            "errors": {
                "name": "WorkflowException",
                "message": (
                    "Validate job trigger rule was failed with 'all_success'."
                ),
            },
        }
