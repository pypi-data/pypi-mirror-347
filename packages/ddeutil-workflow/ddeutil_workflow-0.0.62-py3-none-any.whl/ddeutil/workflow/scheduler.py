# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
"""The main schedule running is `schedule_runner` function that trigger the
multiprocess of `schedule_control` function for listing schedules on the
config by `Loader.finds(Schedule)`.

    The `schedule_control` is the scheduler function that release 2 schedule
functions; `workflow_task`, and `workflow_monitor`.

    `schedule_control` ---( Every minute at :02 )--> `schedule_task`
                       ---( Every 5 minutes     )--> `monitor`

    The `schedule_task` will run `task.release` method in threading object
for multithreading strategy. This `release` method will run only one crontab
value with the on field.

Steps:
    - Extract all schedule config on the conf path.
    - Slice schedules to multiprocess
    - Start running task.
"""
from __future__ import annotations

import copy
import logging
import time
from concurrent.futures import (
    Future,
    ProcessPoolExecutor,
    as_completed,
)
from datetime import datetime, timedelta
from functools import wraps
from heapq import heappop, heappush
from pathlib import Path
from textwrap import dedent
from threading import Thread
from typing import Any, Callable, Optional, TypedDict, Union

from pydantic import BaseModel, Field, ValidationInfo
from pydantic.functional_validators import field_validator, model_validator
from typing_extensions import Self

try:
    from typing import ParamSpec
except ImportError:  # pragma: no cov
    from typing_extensions import ParamSpec

try:
    from schedule import CancelJob
except ImportError:  # pragma: no cov
    CancelJob = None

from .__cron import CronRunner
from .__types import DictData, TupleStr
from .conf import FileLoad, Loader, dynamic
from .event import Crontab
from .exceptions import ScheduleException, WorkflowException
from .logs import Audit, get_audit
from .result import SUCCESS, Result
from .utils import batch, delay
from .workflow import Release, ReleaseQueue, Workflow, WorkflowTask

P = ParamSpec("P")

logging.getLogger("schedule").setLevel(logging.INFO)


__all__: TupleStr = (
    "Schedule",
    "ScheduleWorkflow",
    "schedule_task",
    "monitor",
    "schedule_control",
    "schedule_runner",
    "ReleaseThreads",
    "ReleaseThread",
)


class ScheduleWorkflow(BaseModel):
    """Schedule Workflow Pydantic model that use to keep workflow model for
    the Schedule model. it should not use Workflow model directly because on the
    schedule config it can adjust crontab value that different from the Workflow
    model.

        This on field does not equal to the on field of Workflow model, but it
    uses same logic to generate running release date with crontab object. It
    uses for override the on field if the schedule time was change, but you do
    not want to change on the workflow model.
    """

    extras: DictData = Field(
        default_factory=dict,
        description="An extra parameters that want to override config values.",
    )

    alias: Optional[str] = Field(
        default=None,
        description="An alias name of workflow that use for schedule model.",
    )
    name: str = Field(description="A workflow name.")
    on: list[Crontab] = Field(
        default_factory=list,
        description="An override the list of Crontab object values.",
    )
    values: DictData = Field(
        default_factory=dict,
        description=(
            "A value that want to pass to the workflow params field when auto "
            "calling release method."
        ),
        alias="params",
    )

    @model_validator(mode="before")
    def __prepare_before__(cls, data: Any) -> Any:
        """Prepare incoming values before validating with model fields."""
        if isinstance(data, dict):
            # VALIDATE: Add default the alias field with the name.
            if "alias" not in data:
                data["alias"] = data.get("name")

            cls.__bypass_on(data, extras=data.get("extras"))
        return data

    @classmethod
    def __bypass_on(
        cls, data: DictData, *, extras: Optional[DictData] = None
    ) -> DictData:
        """Bypass and prepare the on data to loaded config data.

        :param data: (DictData) A data that want to validate for the model
            initialization.
        :param extras: (DictData) An extra parameter that want to override core
            config values.

        :rtype: DictData
        """
        if on := data.pop("on", []):

            if isinstance(on, str):
                on: list[str] = [on]

            if any(not isinstance(n, (dict, str)) for n in on):
                raise TypeError("The `on` key should be list of str or dict")

            # NOTE: Pass on value to Loader and keep on model object to on
            #   field.
            data["on"] = [
                FileLoad(n, externals=extras).data if isinstance(n, str) else n
                for n in on
            ]

        return data

    @field_validator("on", mode="after")
    def __on_no_dup__(
        cls, value: list[Crontab], info: ValidationInfo
    ) -> list[Crontab]:
        """Validate the on fields should not contain duplicate values and if it
        contains every minute value, it should have only one on value.

        :param value: (list[Crontab]) A list of `Crontab` object.
        :param info: (ValidationInfo) An validation info object for getting an
            extra parameter.

        :rtype: list[Crontab]
        """
        set_ons: set[str] = {str(on.cronjob) for on in value}
        if len(set_ons) != len(value):
            raise ValueError(
                "The on fields should not contain duplicate on value."
            )

        extras: Optional[DictData] = info.data.get("extras")
        if len(set_ons) > (
            conf := dynamic("max_cron_per_workflow", extras=extras)
        ):
            raise ValueError(
                f"The number of the on should not more than {conf} crontabs."
            )

        return value

    def tasks(
        self,
        start_date: datetime,
        queue: dict[str, ReleaseQueue],
    ) -> list[WorkflowTask]:
        """Return the list of WorkflowTask object from the specific input
        datetime that mapping with the on field.

            This task creation need queue to tracking release date already
        mapped or not.

        :param start_date: (datetime) A start datetime that get from the
            workflow schedule.
        :param queue: (dict[str, ReleaseQueue]) A mapping of name and list of
            datetime for queue.

        :rtype: list[WorkflowTask]
        :return: Return the list of WorkflowTask object from the specific
            input datetime that mapping with the on field.
        """
        wf: Workflow = Workflow.from_conf(self.name, extras=self.extras)
        wf_queue: ReleaseQueue = queue[self.alias]

        # IMPORTANT: Create the default 'on' value if it does not pass the `on`
        #   field to the Schedule object.
        ons: list[Crontab] = self.on or wf.on.copy()
        workflow_tasks: list[WorkflowTask] = []
        for on in ons:

            # NOTE: Create CronRunner instance from the start_date param.
            runner: CronRunner = on.generate(start_date)
            next_running_date = runner.next

            while wf_queue.check_queue(next_running_date):
                next_running_date = runner.next

            workflow_tasks.append(
                WorkflowTask(
                    alias=self.alias,
                    workflow=wf,
                    runner=runner,
                    values=self.values,
                    extras=self.extras,
                ),
            )

        return workflow_tasks


class Schedule(BaseModel):
    """Schedule Pydantic model that use to run with any scheduler package.

        The workflows field of this model include ScheduleWorkflow objects that
    enhance the workflow object by adding the alias and values fields.
    """

    extras: DictData = Field(
        default_factory=dict,
        description="An extra parameters that want to override config values.",
    )

    desc: Optional[str] = Field(
        default=None,
        description=(
            "A schedule description that can be string of markdown content."
        ),
    )
    workflows: list[ScheduleWorkflow] = Field(
        default_factory=list,
        description="A list of ScheduleWorkflow model.",
    )

    @field_validator("desc", mode="after")
    def __dedent_desc__(cls, value: str) -> str:
        """Prepare description string that was created on a template.

        :param value: A description string value that want to dedent.

        :rtype: str
        """
        return dedent(value)

    @classmethod
    def from_conf(
        cls,
        name: str,
        *,
        path: Optional[Path] = None,
        extras: DictData | None = None,
    ) -> Self:
        """Create Schedule instance from the Loader object that only receive
        an input schedule name. The loader object will use this schedule name to
        searching configuration data of this schedule model in conf path.

        :param name: (str) A schedule name that want to pass to Loader object.
        :param path: (Path) An override config path.
        :param extras: An extra parameters that want to pass to Loader
            object.

        :raise ValueError: If the type does not match with current object.

        :rtype: Self
        """
        loader: Loader = FileLoad(name, path=path, extras=extras)

        # NOTE: Validate the config type match with current connection model
        if loader.type != cls.__name__:
            raise ValueError(f"Type {loader.type} does not match with {cls}")

        loader_data: DictData = copy.deepcopy(loader.data)
        loader_data["name"] = name

        if extras:
            loader_data["extras"] = extras

        return cls.model_validate(obj=loader_data)

    def tasks(
        self,
        start_date: datetime,
        queue: dict[str, ReleaseQueue],
    ) -> list[WorkflowTask]:
        """Return the list of WorkflowTask object from the specific input
        datetime that mapping with the on field from workflow schedule model.

        :param start_date: A start date that get from the workflow schedule.
        :param queue: (dict[str, ReleaseQueue]) A mapping of name and list of
            datetime for queue.

        :rtype: list[WorkflowTask]
        :return: Return the list of WorkflowTask object from the specific
            input datetime that mapping with the on field.
        """
        workflow_tasks: list[WorkflowTask] = []

        for workflow in self.workflows:
            if self.extras:
                workflow.extras = self.extras

            if workflow.alias not in queue:
                queue[workflow.alias] = ReleaseQueue()

            workflow_tasks.extend(workflow.tasks(start_date, queue=queue))

        return workflow_tasks

    def pending(
        self,
        *,
        stop: Optional[datetime] = None,
        audit: type[Audit] | None = None,
        parent_run_id: Optional[str] = None,
    ) -> Result:  # pragma: no cov
        """Pending this schedule tasks with the schedule package.

        :param stop: A datetime value that use to stop running schedule.
        :param audit: An audit class that use on the workflow task release for
            writing its release audit context.
        :param parent_run_id: A parent workflow running ID for this release.
        """
        audit: type[Audit] = audit or get_audit(extras=self.extras)
        result: Result = Result().set_parent_run_id(parent_run_id)

        # NOTE: Create the start and stop datetime.
        start_date: datetime = datetime.now(
            tz=dynamic("tz", extras=self.extras)
        )
        stop_date: datetime = stop or (
            start_date + dynamic("stop_boundary_delta", extras=self.extras)
        )

        # IMPORTANT: Create main mapping of queue and thread object.
        queue: dict[str, ReleaseQueue] = {}
        threads: ReleaseThreads = {}

        start_date_waiting: datetime = start_date.replace(
            second=0, microsecond=0
        ) + timedelta(minutes=1)

        scheduler_pending(
            tasks=self.tasks(start_date_waiting, queue=queue),
            stop=stop_date,
            queue=queue,
            threads=threads,
            result=result,
            audit=audit,
        )

        return result.catch(status=SUCCESS)


ResultOrCancel = Union[type[CancelJob], Result]
ReturnResultOrCancel = Callable[P, ResultOrCancel]
DecoratorCancelJob = Callable[[ReturnResultOrCancel], ReturnResultOrCancel]


def catch_exceptions(
    cancel_on_failure: bool = False,
    parent_run_id: Optional[str] = None,
) -> DecoratorCancelJob:
    """Catch exception error from scheduler job that running with schedule
    package and return CancelJob if this function raise an error.

    :param cancel_on_failure: A flag that allow to return the CancelJob or not
        it will raise.
    :param parent_run_id:

    :rtype: DecoratorCancelJob
    """

    def decorator(
        func: ReturnResultOrCancel,
    ) -> ReturnResultOrCancel:  # pragma: no cov

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> ResultOrCancel:

            try:
                return func(*args, **kwargs)

            except Exception as err:
                if parent_run_id:
                    (
                        Result(parent_run_id=parent_run_id).trace.exception(
                            str(err)
                        )
                    )
                if cancel_on_failure:
                    return CancelJob
                raise err

        return wrapper

    return decorator


class ReleaseThread(TypedDict):
    """TypeDict for the release thread."""

    thread: Optional[Thread]
    start_date: datetime
    release_date: datetime


ReleaseThreads = dict[str, ReleaseThread]


def schedule_task(
    tasks: list[WorkflowTask],
    stop: datetime,
    queue: dict[str, ReleaseQueue],
    threads: ReleaseThreads,
    audit: type[Audit],
    *,
    parent_run_id: Optional[str] = None,
    extras: Optional[DictData] = None,
) -> ResultOrCancel:
    """Schedule task function that generate thread of workflow task release
    method in background. This function do the same logic as the workflow poke
    method, but it runs with map of schedules and the on values.

        This schedule task start runs every minute at ':02' second, and it does
    not allow you to run with offset time.

    :param tasks: A list of WorkflowTask object.
    :param stop: A stop datetime object that force stop running scheduler.
    :param queue: A mapping of alias name and ReleaseQueue object.
    :param threads: A mapping of alias name and Thread object.
    :param audit: An audit class that want to make audit object.
    :param parent_run_id: A parent workflow running ID for this release.
    :param extras: An extra parameter that want to override the core config.

    :rtype: ResultOrCancel
    """
    result: Result = Result().set_parent_run_id(parent_run_id)
    current_date: datetime = datetime.now(tz=dynamic("tz", extras=extras))
    if current_date > stop.replace(tzinfo=dynamic("tz", extras=extras)):
        return CancelJob

    # IMPORTANT:
    #       Filter workflow & on that should to run with `workflow_release`
    #   function. It will deplicate running with different schedule value
    #   because I use current time in this condition.
    #
    #       For example, if a queue has a time release be '00:02:00' that should
    #   to run and its schedule has '*/2 * * * *' and '*/35 * * * *'.
    #   This condition make this function create 2 threading tasks.
    #
    #       '00:02:00'  --> '*/2 * * * *'   --> run
    #                   --> '*/35 * * * *'  --> skip
    #
    for task in tasks:

        # NOTE: Get the ReleaseQueue with an alias of the WorkflowTask.
        q: ReleaseQueue = queue[task.alias]

        # NOTE: Start adding queue and move the runner date in the WorkflowTask.
        task.queue(stop, q, audit=audit)

        # NOTE: Get incoming datetime queue.
        result.trace.debug(
            f"[WORKFLOW]: Queue: {task.alias!r} : {list(q.queue)}"
        )

        # VALIDATE: Check the queue is empty or not.
        if not q.is_queued:
            result.trace.warning(
                f"[WORKFLOW]: Queue is empty for : {task.alias!r} : "
                f"{task.runner.cron}"
            )
            continue

        # VALIDATE: Check this task is the first release in the queue or not.
        current_release: datetime = current_date.replace(
            second=0, microsecond=0
        )
        if (first_date := q.queue[0].date) > current_release:  # pragma: no cov
            result.trace.debug(
                f"[WORKFLOW]: Skip schedule "
                f"{first_date:%Y-%m-%d %H:%M:%S} for : {task.alias!r}"
            )
            continue
        elif first_date < current_release:  # pragma: no cov
            raise ScheduleException(
                "The first release date from queue should not less than current"
                "release date."
            )

        # NOTE: Pop the latest release and push it to running.
        release: Release = heappop(q.queue)
        heappush(q.running, release)

        result.trace.info(
            f"[WORKFLOW]: Start thread: '{task.alias}|"
            f"{release.date:%Y%m%d%H%M}'"
        )

        # NOTE: Create thread name that able to tracking with observe schedule
        #   job.
        thread_name: str = f"{task.alias}|{release.date:%Y%m%d%H%M}"
        thread: Thread = Thread(
            target=catch_exceptions(
                cancel_on_failure=True,
            )(task.release),
            kwargs={
                "release": release,
                "queue": q,
                "audit": audit,
            },
            name=thread_name,
            daemon=True,
        )

        threads[thread_name] = {
            "thread": thread,
            "start_date": datetime.now(tz=dynamic("tz", extras=extras)),
            "release_date": release.date,
        }

        thread.start()

        delay()

    result.trace.debug(
        f"[SCHEDULE]: End schedule task that run since "
        f"{current_date:%Y-%m-%d %H:%M:%S} {'=' * 30}"
    )
    return result.catch(status=SUCCESS, context={"task_date": current_date})


def monitor(
    threads: ReleaseThreads,
    parent_run_id: Optional[str] = None,
) -> None:  # pragma: no cov
    """Monitoring function that running every five minute for track long-running
    thread instance from the schedule_control function that run every minute.

    :param threads: A mapping of Thread object and its name.
    :param parent_run_id: A parent workflow running ID for this release.

    :type threads: ReleaseThreads
    """
    result: Result = Result().set_parent_run_id(parent_run_id)
    result.trace.debug("[MONITOR]: Start checking long running schedule task.")

    snapshot_threads: list[str] = list(threads.keys())
    for thread_name in snapshot_threads:

        thread_release: ReleaseThread = threads[thread_name]

        # NOTE: remove the thread that running success.
        thread = thread_release["thread"]
        if thread and (not thread_release["thread"].is_alive()):
            thread_release["thread"] = None


def scheduler_pending(
    tasks: list[WorkflowTask],
    stop: datetime,
    queue: dict[str, ReleaseQueue],
    threads: ReleaseThreads,
    result: Result,
    audit: type[Audit],
) -> Result:  # pragma: no cov
    """Scheduler pending function.

    :param tasks: A list of WorkflowTask object.
    :param stop: A stop datetime object that force stop running scheduler.
    :param queue: A mapping of alias name and ReleaseQueue object.
    :param threads: A mapping of alias name and Thread object.
    :param result: A result object.
    :param audit: An audit class that want to make audit object.

    :rtype: Result
    """
    try:
        from schedule import Scheduler
    except ImportError:
        raise ImportError(
            "Should install schedule package before use this method."
        ) from None

    scheduler: Scheduler = Scheduler()

    # NOTE: This schedule job will start every minute at :02 seconds.
    (
        scheduler.every(1)
        .minutes.at(":02")
        .do(
            catch_exceptions(
                cancel_on_failure=True,
                parent_run_id=result.parent_run_id,
            )(schedule_task),
            tasks=tasks,
            stop=stop,
            queue=queue,
            threads=threads,
            audit=audit,
            parent_run_id=result.parent_run_id,
        )
        .tag("control")
    )

    # NOTE: Checking zombie task with schedule job will start every 5 minute at
    #   :10 seconds.
    (
        scheduler.every(5)
        .minutes.at(":10")
        .do(
            monitor,
            threads=threads,
            parent_run_id=result.parent_run_id,
        )
        .tag("monitor")
    )

    # NOTE: Start running schedule
    result.trace.info(
        f"[SCHEDULE]: Schedule with stopper: {stop:%Y-%m-%d %H:%M:%S}"
    )

    while True:
        scheduler.run_pending()
        time.sleep(1)

        # NOTE: Break the scheduler when the control job does not exist.
        if not scheduler.get_jobs("control"):
            scheduler.clear("monitor")

            while len([t for t in threads.values() if t["thread"]]) > 0:
                result.trace.warning(
                    "[SCHEDULE]: Waiting schedule release thread that still "
                    "running in background."
                )
                delay(10)
                monitor(threads, parent_run_id=result.parent_run_id)

            break

    result.trace.warning(
        f"[SCHEDULE]: Queue: {[list(queue[wf].queue) for wf in queue]}"
    )
    return result.catch(
        status=SUCCESS,
        context={
            "threads": [
                {
                    "name": thread,
                    "start_date": threads[thread]["start_date"],
                    "release_date": threads[thread]["release_date"],
                }
                for thread in threads
            ],
        },
    )


def schedule_control(
    schedules: list[str],
    stop: Optional[datetime] = None,
    *,
    extras: DictData | None = None,
    audit: type[Audit] | None = None,
    parent_run_id: Optional[str] = None,
) -> Result:  # pragma: no cov
    """Scheduler control function that run the chuck of schedules every minute
    and this function release monitoring thread for tracking undead thread in
    the background.

    :param schedules: A list of workflow names that want to schedule running.
    :param stop: A datetime value that use to stop running schedule.
    :param extras: An extra parameters that want to override core config.
    :param audit: An audit class that use on the workflow task release for
        writing its release audit context.
    :param parent_run_id: A parent workflow running ID for this release.

    :rtype: Result
    """
    audit: type[Audit] = audit or get_audit(extras=extras)
    result: Result = Result.construct_with_rs_or_id(parent_run_id=parent_run_id)

    # NOTE: Create the start and stop datetime.
    start_date: datetime = datetime.now(tz=dynamic("tz", extras=extras))
    stop_date: datetime = stop or (
        start_date + dynamic("stop_boundary_delta", extras=extras)
    )

    # IMPORTANT: Create main mapping of queue and thread object.
    queue: dict[str, ReleaseQueue] = {}
    threads: ReleaseThreads = {}

    start_date_waiting: datetime = start_date.replace(
        second=0, microsecond=0
    ) + timedelta(minutes=1)

    tasks: list[WorkflowTask] = []
    for name in schedules:
        tasks.extend(
            (
                Schedule.from_conf(name, extras=extras).tasks(
                    start_date_waiting, queue=queue
                )
            ),
        )

    scheduler_pending(
        tasks=tasks,
        stop=stop_date,
        queue=queue,
        threads=threads,
        result=result,
        audit=audit,
    )

    return result.catch(status=SUCCESS, context={"schedules": schedules})


def schedule_runner(
    stop: Optional[datetime] = None,
    *,
    max_process: int | None = None,
    extras: DictData | None = None,
    excluded: list[str] | None = None,
) -> Result:  # pragma: no cov
    """Schedule runner function it the multiprocess controller function for
    split the setting schedule to the `schedule_control` function on the
    process pool. It chunks schedule configs that exists in config
    path by `WORKFLOW_APP_MAX_SCHEDULE_PER_PROCESS` value.

    :param stop: A stop datetime object that force stop running scheduler.
    :param max_process: (int) The maximum process that want to run this func.
    :param extras: An extra parameter that want to override core config.
    :param excluded: A list of schedule name that want to exclude from finding.

        This function will get all workflows that include on value that was
    created in config path and chuck it with application config variable
    `WORKFLOW_APP_MAX_SCHEDULE_PER_PROCESS` env var to multiprocess executor
    pool.

        The current workflow logic that split to process will be below diagram:

        MAIN ==> process 01 ==> schedule ==> thread 01 --> 01
                                         ==> thread 01 --> 02
                            ==> schedule ==> thread 02 --> 01
                                         ==> thread 02 --> 02
                                         ==> ...
            ==> process 02  ==> ...

    :rtype: Result
    """
    result: Result = Result()
    context: DictData = {"schedules": [], "threads": []}

    with ProcessPoolExecutor(
        max_workers=dynamic(
            "max_schedule_process", f=max_process, extras=extras
        ),
    ) as executor:

        futures: list[Future] = [
            executor.submit(
                schedule_control,
                schedules=[load[0] for load in loader],
                stop=stop,
                extras=extras,
                parent_run_id=result.parent_run_id,
            )
            for loader in batch(
                Loader.finds(Schedule, excluded=excluded),
                n=dynamic("max_schedule_per_process", extras=extras),
            )
        ]

        for future in as_completed(futures):

            # NOTE: Raise error when it has any error from schedule_control.
            if err := future.exception():
                result.trace.error(str(err))
                raise WorkflowException(str(err)) from err

            rs: Result = future.result(timeout=1)
            context["schedule"].extend(rs.context.get("schedules", []))
            context["threads"].extend(rs.context.get("threads", []))

    return result.catch(status=SUCCESS, context=context)
