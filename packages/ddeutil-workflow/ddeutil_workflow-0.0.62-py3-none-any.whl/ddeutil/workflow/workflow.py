# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
"""Workflow module is the core module of this package. It keeps Release,
ReleaseQueue, and Workflow models.

    This package implement timeout strategy on the workflow execution layer only
because the main propose of this package is using Workflow to be orchestrator.

    ReleaseQueue is the memory storage of Release for tracking this release
already run or pending in the current session.
"""
from __future__ import annotations

import copy
import time
from concurrent.futures import (
    Future,
    ThreadPoolExecutor,
    as_completed,
)
from dataclasses import field
from datetime import datetime, timedelta
from enum import Enum
from functools import partial, total_ordering
from heapq import heappop, heappush
from pathlib import Path
from queue import Queue
from textwrap import dedent
from threading import Event, Lock
from typing import Any, Optional, Union
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo
from pydantic.dataclasses import dataclass
from pydantic.functional_validators import field_validator, model_validator
from typing_extensions import Self

from .__cron import CronRunner
from .__types import DictData
from .conf import FileLoad, Loader, dynamic
from .event import Crontab
from .exceptions import WorkflowException
from .job import Job
from .logs import Audit, get_audit
from .params import Param
from .result import CANCEL, FAILED, SKIP, SUCCESS, WAIT, Result
from .reusables import has_template, param2template
from .utils import (
    clear_tz,
    gen_id,
    get_dt_now,
    reach_next_minute,
    replace_sec,
    wait_until_next_minute,
)


class ReleaseType(str, Enum):
    """Release Type Enum support the type field on the Release dataclass."""

    DEFAULT = "manual"
    SCHEDULE = "schedule"
    POKING = "poking"
    FORCE = "force"


@total_ordering
@dataclass(config=ConfigDict(use_enum_values=True))
class Release:
    """Release object that use for represent the release datetime."""

    date: datetime = Field(
        description=(
            "A release date that should has second and millisecond equal 0."
        )
    )
    type: ReleaseType = Field(
        default=ReleaseType.DEFAULT,
        description="A type of release that create before start execution.",
    )

    def __repr__(self) -> str:
        """Override __repr__ method for represent value of `date` field.

        :rtype: str
        """
        return repr(f"{self.date:%Y-%m-%d %H:%M:%S}")

    def __str__(self) -> str:
        """Override string value of this release object with the `date` field.

        :rtype: str
        """
        return f"{self.date:%Y-%m-%d %H:%M:%S}"

    @classmethod
    def from_dt(cls, dt: Union[datetime, str]) -> Self:
        """Construct Release object from `datetime` or `str` objects.

            This method will replace second and millisecond value to 0 and
        replace timezone to the `tz` config setting or extras overriding before
        create Release object.

        :param dt: (Union[datetime, str]) A datetime object or string that want to
            construct to the Release object.

        :raise TypeError: If the type of the dt argument does not valid with
            datetime or str object.

        :rtype: Release
        """
        if isinstance(dt, str):
            dt: datetime = datetime.fromisoformat(dt)
        elif not isinstance(dt, datetime):
            raise TypeError(
                f"The `from_dt` need the `dt` parameter type be `str` or "
                f"`datetime` only, not {type(dt)}."
            )
        return cls(date=replace_sec(dt.replace(tzinfo=None)))

    def __eq__(self, other: Union[Release, datetime]) -> bool:
        """Override equal property that will compare only the same type or
        datetime.

        :rtype: bool
        """
        if isinstance(other, self.__class__):
            return self.date == other.date
        elif isinstance(other, datetime):
            return self.date == other
        return NotImplemented

    def __lt__(self, other: Union[Release, datetime]) -> bool:
        """Override less-than property that will compare only the same type or
        datetime.

        :rtype: bool
        """
        if isinstance(other, self.__class__):
            return self.date < other.date
        elif isinstance(other, datetime):
            return self.date < other
        return NotImplemented


class ReleaseQueue:
    """ReleaseQueue object that is storage management of Release objects on
    the memory with list object.
    """

    def __init__(
        self,
        queue: Optional[list[Release]] = None,
        running: Optional[list[Release]] = None,
        complete: Optional[list[Release]] = None,
        extras: Optional[DictData] = None,
    ):
        self.queue: list[Release] = queue or []
        self.running: list[Release] = running or []
        self.complete: list[Release] = complete or []
        self.extras: DictData = extras or {}
        self.lock: Lock = Lock()

    @classmethod
    def from_list(
        cls,
        queue: Optional[Union[list[datetime], list[Release]]] = None,
    ) -> Self:
        """Construct ReleaseQueue object from an input queue value that passing
        with list of datetime or list of Release.

        :param queue: A queue object for create ReleaseQueue instance.

        :raise TypeError: If the type of input queue does not valid.

        :rtype: ReleaseQueue
        """
        if queue is None:
            return cls()

        if isinstance(queue, list):
            if all(isinstance(q, datetime) for q in queue):
                return cls(queue=[Release.from_dt(q) for q in queue])

            if all(isinstance(q, Release) for q in queue):
                return cls(queue=queue)

        raise TypeError(
            "Type of the queue does not valid with ReleaseQueue "
            "or list of datetime or list of Release."
        )

    @property
    def is_queued(self) -> bool:
        """Return True if it has workflow release object in the queue.

        :rtype: bool
        """
        return len(self.queue) > 0

    def check_queue(self, value: Union[Release, datetime]) -> bool:
        """Check a Release value already exists in list of tracking
        queues.

        :param value: A Release object that want to check it already in
            queues.

        :rtype: bool
        """
        if isinstance(value, datetime):
            value = Release.from_dt(value)

        with self.lock:
            return (
                (value in self.queue)
                or (value in self.running)
                or (value in self.complete)
            )

    def mark_complete(self, value: Release) -> Self:
        """Push Release to the complete queue. After push the release, it will
        delete old release base on the `CORE_MAX_QUEUE_COMPLETE_HIST` value.

        :param value: (Release) A Release value that want to push to the
            complete field.

        :rtype: Self
        """
        with self.lock:
            if value in self.running:
                self.running.remove(value)

            heappush(self.complete, value)

            # NOTE: Remove complete queue on workflow that keep more than the
            #   maximum config value.
            num_complete_delete: int = len(self.complete) - dynamic(
                "max_queue_complete_hist", extras=self.extras
            )

            if num_complete_delete > 0:
                for _ in range(num_complete_delete):
                    heappop(self.complete)

        return self

    def gen(
        self,
        end_date: datetime,
        audit: type[Audit],
        runner: CronRunner,
        name: str,
        *,
        force_run: bool = False,
        extras: Optional[DictData] = None,
    ) -> Self:
        """Generate a Release model to the queue field with an input CronRunner.

        Steps:
            - Create Release object from the current date that not reach the end
              date.
            - Check this release do not store on the release queue object.
              Generate the next date if it exists.
            - Push this release to the release queue

        :param end_date: (datetime) An end datetime object.
        :param audit: (type[Audit]) An audit class that want to make audit
            instance.
        :param runner: (CronRunner) A `CronRunner` object.
        :param name: (str) A target name that want to check at pointer of audit.
        :param force_run: (bool) A flag that allow to release workflow if the
            audit with that release was pointed. (Default is False).
        :param extras: (DictDatA) An extra parameter that want to override core
            config values.

        :rtype: ReleaseQueue

        """
        if clear_tz(runner.date) > clear_tz(end_date):
            return self

        release = Release(
            date=clear_tz(runner.date),
            type=(ReleaseType.FORCE if force_run else ReleaseType.POKING),
        )

        while self.check_queue(release) or (
            audit.is_pointed(name=name, release=release.date, extras=extras)
            and not force_run
        ):
            release = Release(
                date=clear_tz(runner.next),
                type=(ReleaseType.FORCE if force_run else ReleaseType.POKING),
            )

        if clear_tz(runner.date) > clear_tz(end_date):
            return self

        with self.lock:
            heappush(self.queue, release)

        return self


class Workflow(BaseModel):
    """Workflow model that use to keep the `Job` and `Crontab` models.

        This is the main future of this project because it uses to be workflow
    data for running everywhere that you want or using it to scheduler task in
    background. It uses lightweight coding line from Pydantic Model and enhance
    execute method on it.
    """

    extras: DictData = Field(
        default_factory=dict,
        description="An extra parameters that want to override config values.",
    )

    name: str = Field(description="A workflow name.")
    desc: Optional[str] = Field(
        default=None,
        description=(
            "A workflow description that can be string of markdown content."
        ),
    )
    params: dict[str, Param] = Field(
        default_factory=dict,
        description="A parameters that need to use on this workflow.",
    )
    on: list[Crontab] = Field(
        default_factory=list,
        description="A list of Crontab instance for this workflow schedule.",
    )
    jobs: dict[str, Job] = Field(
        default_factory=dict,
        description="A mapping of job ID and job model that already loaded.",
    )

    @classmethod
    def from_conf(
        cls,
        name: str,
        *,
        path: Optional[Path] = None,
        extras: DictData | None = None,
        loader: type[Loader] = None,
    ) -> Self:
        """Create Workflow instance from the Loader object that only receive
        an input workflow name. The loader object will use this workflow name to
        searching configuration data of this workflow model in conf path.

        :param name: (str) A workflow name that want to pass to Loader object.
        :param path: (Path) An override config path.
        :param extras: (DictData) An extra parameters that want to override core
            config values.
        :param loader: A loader class for override default loader object.

        :raise ValueError: If the type does not match with current object.

        :rtype: Self
        """
        loader: type[Loader] = loader or FileLoad
        load: Loader = loader(name, path=path, extras=extras)

        # NOTE: Validate the config type match with current connection model
        if load.type != cls.__name__:
            raise ValueError(f"Type {load.type} does not match with {cls}")

        data: DictData = copy.deepcopy(load.data)
        data["name"] = name

        if extras:
            data["extras"] = extras

        cls.__bypass_on__(data, path=load.path, extras=extras, loader=loader)
        return cls.model_validate(obj=data)

    @classmethod
    def __bypass_on__(
        cls,
        data: DictData,
        path: Path,
        extras: DictData | None = None,
        loader: type[Loader] = None,
    ) -> DictData:
        """Bypass the on data to loaded config data.

        :param data: (DictData) A data to construct to this Workflow model.
        :param path: (Path) A config path.
        :param extras: (DictData) An extra parameters that want to override core
            config values.

        :rtype: DictData
        """
        if on := data.pop("on", []):
            if isinstance(on, str):
                on: list[str] = [on]
            if any(not isinstance(i, (dict, str)) for i in on):
                raise TypeError("The `on` key should be list of str or dict")

            # NOTE: Pass on value to SimLoad and keep on model object to the on
            #   field.
            data["on"] = [
                (
                    (loader or FileLoad)(n, path=path, extras=extras).data
                    if isinstance(n, str)
                    else n
                )
                for n in on
            ]
        return data

    @model_validator(mode="before")
    def __prepare_model_before__(cls, data: Any) -> Any:
        """Prepare the params key in the data model before validating."""
        if isinstance(data, dict) and (params := data.pop("params", {})):
            data["params"] = {
                p: (
                    {"type": params[p]}
                    if isinstance(params[p], str)
                    else params[p]
                )
                for p in params
            }
        return data

    @field_validator("desc", mode="after")
    def __dedent_desc__(cls, value: str) -> str:
        """Prepare description string that was created on a template.

        :param value: A description string value that want to dedent.
        :rtype: str
        """
        return dedent(value.lstrip("\n"))

    @field_validator("on", mode="after")
    def __on_no_dup_and_reach_limit__(
        cls,
        value: list[Crontab],
        info: ValidationInfo,
    ) -> list[Crontab]:
        """Validate the on fields should not contain duplicate values and if it
        contains the every minute value more than one value, it will remove to
        only one value.

        :raise ValueError: If it has some duplicate value.

        :param value: A list of on object.

        :rtype: list[Crontab]
        """
        set_ons: set[str] = {str(on.cronjob) for on in value}
        if len(set_ons) != len(value):
            raise ValueError(
                "The on fields should not contain duplicate on value."
            )

        # WARNING:
        # if '* * * * *' in set_ons and len(set_ons) > 1:
        #     raise ValueError(
        #         "If it has every minute cronjob on value, it should have "
        #         "only one value in the on field."
        #     )
        set_tz: set[str] = {on.tz for on in value}
        if len(set_tz) > 1:
            raise ValueError(
                f"The on fields should not contain multiple timezone, "
                f"{list(set_tz)}."
            )

        extras: Optional[DictData] = info.data.get("extras")
        if len(set_ons) > (
            conf := dynamic("max_cron_per_workflow", extras=extras)
        ):
            raise ValueError(
                f"The number of the on should not more than {conf} crontabs."
            )
        return value

    @model_validator(mode="after")
    def __validate_jobs_need__(self) -> Self:
        """Validate each need job in any jobs should exist.

        :raise WorkflowException: If it has not exists need value in this
            workflow job.

        :rtype: Self
        """
        for job in self.jobs:
            if not_exist := [
                need for need in self.jobs[job].needs if need not in self.jobs
            ]:
                raise WorkflowException(
                    f"The needed jobs: {not_exist} do not found in "
                    f"{self.name!r}."
                )

            self.jobs[job].id = job

        # VALIDATE: Validate workflow name should not dynamic with params
        #   template.
        if has_template(self.name):
            raise ValueError(
                f"Workflow name should not has any template, please check, "
                f"{self.name!r}."
            )

        return self

    def job(self, name: str) -> Job:
        """Return the workflow's Job model that getting by an input job's name
        or job's ID. This method will pass an extra parameter from this model
        to the returned Job model.

        :param name: (str) A job name or ID that want to get from a mapping of
            job models.

        :raise ValueError: If a name or ID does not exist on the jobs field.

        :rtype: Job
        :return: A job model that exists on this workflow by input name.
        """
        if name not in self.jobs:
            raise ValueError(
                f"A Job {name!r} does not exists in this workflow, "
                f"{self.name!r}"
            )
        job: Job = self.jobs[name]
        if self.extras:
            job.extras = self.extras
        return job

    def parameterize(self, params: DictData) -> DictData:
        """Prepare a passing parameters before use it in execution process.
        This method will validate keys of an incoming params with this object
        necessary params field and then create a jobs key to result mapping
        that will keep any execution result from its job.

            ... {
            ...     "params": <an-incoming-params>,
            ...     "jobs": {}
            ... }

        :param params: (DictData) A parameter data that receive from workflow
            execute method.

        :raise WorkflowException: If parameter value that want to validate does
            not include the necessary parameter that had required flag.

        :rtype: DictData
        :return: The parameter value that validate with its parameter fields and
            adding jobs key to this parameter.
        """
        # VALIDATE: Incoming params should have keys that set on this workflow.
        check_key: list[str] = [
            f"{k!r}"
            for k in self.params
            if (k not in params and self.params[k].required)
        ]
        if check_key:
            raise WorkflowException(
                f"Required Param on this workflow setting does not set: "
                f"{', '.join(check_key)}."
            )

        # NOTE: Mapping type of param before adding it to the `params` key.
        return {
            "params": (
                params
                | {
                    k: self.params[k].receive(params[k])
                    for k in params
                    if k in self.params
                }
            ),
            "jobs": {},
        }

    def release(
        self,
        release: Union[Release, datetime],
        params: DictData,
        *,
        run_id: Optional[str] = None,
        parent_run_id: Optional[str] = None,
        audit: type[Audit] = None,
        queue: Optional[ReleaseQueue] = None,
        override_log_name: Optional[str] = None,
        result: Optional[Result] = None,
        timeout: int = 600,
    ) -> Result:
        """Release the workflow which is executes workflow with writing audit
        log tracking. The method is overriding parameter with the release
        templating that include logical date (release date), execution date,
        or running id to the params.

            This method allow workflow use audit object to save the execution
        result to audit destination like file audit to the local `./logs` path.

        Steps:
            - Initialize Release and validate ReleaseQueue.
            - Create release data for pass to parameter templating function.
            - Execute this workflow with mapping release data to its parameters.
            - Writing result audit
            - Remove this release on the running queue
            - Push this release to complete queue

        :param release: A release datetime or Release object.
        :param params: A workflow parameter that pass to execute method.
        :param run_id: (str) A workflow running ID.
        :param parent_run_id: (str) A parent workflow running ID.
        :param audit: An audit class that want to save the execution result.
        :param queue: (ReleaseQueue) A ReleaseQueue object.
        :param override_log_name: (str) An override logging name that use
            instead the workflow name.
        :param result: (Result) A result object for keeping context and status
            data.
        :param timeout: (int) A workflow execution time out in second unit.

        :raise TypeError: If a queue parameter does not match with ReleaseQueue
            type.

        :rtype: Result
        """
        audit: type[Audit] = audit or get_audit(extras=self.extras)
        name: str = override_log_name or self.name
        result: Result = Result.construct_with_rs_or_id(
            result,
            run_id=run_id,
            parent_run_id=parent_run_id,
            id_logic=name,
            extras=self.extras,
        )

        # VALIDATE: check type of queue that valid with ReleaseQueue.
        if queue is not None and not isinstance(queue, ReleaseQueue):
            raise TypeError(
                "The queue argument should be ReleaseQueue object only."
            )

        # VALIDATE: Change release value to Release object.
        if isinstance(release, datetime):
            release: Release = Release.from_dt(release)

        result.trace.info(
            f"[RELEASE]: Start {name!r} : {release.date:%Y-%m-%d %H:%M:%S}"
        )
        tz: ZoneInfo = dynamic("tz", extras=self.extras)
        values: DictData = param2template(
            params,
            params={
                "release": {
                    "logical_date": release.date,
                    "execute_date": datetime.now(tz=tz),
                    "run_id": result.run_id,
                }
            },
            extras=self.extras,
        )
        rs: Result = self.execute(
            params=values,
            result=result,
            parent_run_id=result.run_id,
            timeout=timeout,
        )
        result.trace.info(
            f"[RELEASE]: End {name!r} : {release.date:%Y-%m-%d %H:%M:%S}"
        )
        result.trace.debug(f"[RELEASE]: Writing audit: {name!r}.")
        (
            audit(
                name=name,
                release=release.date,
                type=release.type,
                context=result.context,
                parent_run_id=result.parent_run_id,
                run_id=result.run_id,
                execution_time=result.alive_time(),
                extras=self.extras,
            ).save(excluded=None)
        )

        if queue:
            queue.mark_complete(release)

        return result.catch(
            status=rs.status,
            context={
                "params": params,
                "release": {
                    "type": release.type,
                    "logical_date": release.date,
                },
                **{"jobs": result.context.pop("jobs", {})},
                **(
                    result.context["errors"]
                    if "errors" in result.context
                    else {}
                ),
            },
        )

    def execute_job(
        self,
        job: Job,
        params: DictData,
        *,
        result: Optional[Result] = None,
        event: Optional[Event] = None,
    ) -> Result:
        """Job execution with passing dynamic parameters from the main workflow
        execution to the target job object via job's ID.

            This execution is the minimum level of execution of this workflow
        model. It different with `self.execute` because this method run only
        one job and return with context of this job data.

        :raise WorkflowException: If the job execution raise JobException.

        :param job: (Job) A job model that want to execute.
        :param params: (DictData) A parameter data.
        :param result: (Result) A Result instance for return context and status.
        :param event: (Event) An Event manager instance that use to cancel this
            execution if it forces stopped by parent execution.

        :rtype: Result
        """
        result: Result = result or Result(run_id=gen_id(self.name, unique=True))

        if job.is_skipped(params=params):
            result.trace.info(f"[WORKFLOW]: Skip Job: {job.id!r}")
            job.set_outputs(output={"skipped": True}, to=params)
            return result.catch(status=SKIP, context=params)

        if event and event.is_set():
            return result.catch(
                status=CANCEL,
                context={
                    "errors": WorkflowException(
                        "Workflow job was canceled because event was set."
                    ).to_dict(),
                },
            )

        result.trace.info(f"[WORKFLOW]: Execute Job: {job.id!r}")
        rs: Result = job.execute(
            params=params,
            run_id=result.run_id,
            parent_run_id=result.parent_run_id,
            event=event,
        )
        job.set_outputs(rs.context, to=params)
        if rs.status in (FAILED, CANCEL):
            error_msg: str = (
                f"Job, {job.id!r}, return `{rs.status.name}` status."
            )
            return result.catch(
                status=rs.status,
                context={
                    "errors": WorkflowException(error_msg).to_dict(),
                    **params,
                },
            )
        return result.catch(status=SUCCESS, context=params)

    def execute(
        self,
        params: DictData,
        *,
        run_id: Optional[str] = None,
        parent_run_id: Optional[str] = None,
        result: Optional[Result] = None,
        event: Optional[Event] = None,
        timeout: float = 3600,
        max_job_parallel: int = 2,
    ) -> Result:
        """Execute workflow with passing a dynamic parameters to all jobs that
        included in this workflow model with `jobs` field.

            The result of execution process for each job and stages on this
        workflow will keep in dict which able to catch out with all jobs and
        stages by dot annotation.

            For example with non-strategy job, when I want to use the output
        from previous stage, I can access it with syntax:

        ... ${job-id}.stages.${stage-id}.outputs.${key}
        ... ${job-id}.stages.${stage-id}.errors.${key}

            But example for strategy job:

        ... ${job-id}.strategies.${strategy-id}.stages.${stage-id}.outputs.${key}
        ... ${job-id}.strategies.${strategy-id}.stages.${stage-id}.errors.${key}

            This method already handle all exception class that can raise from
        the job execution. It will warp that error and keep it in the key `errors`
        at the result context.

        :param params: A parameter data that will parameterize before execution.
        :param run_id: (Optional[str]) A workflow running ID.
        :param parent_run_id: (Optional[str]) A parent workflow running ID.
        :param result: (Result) A Result instance for return context and status.
        :param event: (Event) An Event manager instance that use to cancel this
            execution if it forces stopped by parent execution.
        :param timeout: (float) A workflow execution time out in second unit
            that use for limit time of execution and waiting job dependency.
            This value does not force stop the task that still running more than
            this limit time. (Default: 60 * 60 seconds)
        :param max_job_parallel: (int) The maximum workers that use for job
            execution in `PoolThreadExecutor` object. (Default: 2 workers)

        :rtype: Result
        """
        ts: float = time.monotonic()
        result: Result = Result.construct_with_rs_or_id(
            result,
            run_id=run_id,
            parent_run_id=parent_run_id,
            id_logic=self.name,
            extras=self.extras,
        )
        context: DictData = self.parameterize(params)
        event: Event = event or Event()
        max_job_parallel: int = dynamic(
            "max_job_parallel", f=max_job_parallel, extras=self.extras
        )
        result.trace.info(
            f"[WORKFLOW]: Execute: {self.name!r} ("
            f"{'parallel' if max_job_parallel > 1 else 'sequential'} jobs)"
        )
        if not self.jobs:
            result.trace.warning(f"[WORKFLOW]: {self.name!r} does not set jobs")
            return result.catch(status=SUCCESS, context=context)

        job_queue: Queue = Queue()
        for job_id in self.jobs:
            job_queue.put(job_id)

        not_timeout_flag: bool = True
        timeout: float = dynamic(
            "max_job_exec_timeout", f=timeout, extras=self.extras
        )

        with ThreadPoolExecutor(
            max_workers=max_job_parallel, thread_name_prefix="wf_exec_"
        ) as executor:
            futures: list[Future] = []

            while not job_queue.empty() and (
                not_timeout_flag := ((time.monotonic() - ts) < timeout)
            ):
                job_id: str = job_queue.get()
                job: Job = self.job(name=job_id)
                if (check := job.check_needs(context["jobs"])) == WAIT:
                    job_queue.task_done()
                    job_queue.put(job_id)
                    time.sleep(0.15)
                    continue
                elif check == FAILED:  # pragma: no cov
                    return result.catch(
                        status=FAILED,
                        context={
                            "errors": WorkflowException(
                                f"Validate job trigger rule was failed with "
                                f"{job.trigger_rule.value!r}."
                            ).to_dict()
                        },
                    )
                elif check == SKIP:  # pragma: no cov
                    result.trace.info(f"[JOB]: Skip job: {job_id!r}")
                    job.set_outputs(output={"skipped": True}, to=context)
                    job_queue.task_done()
                    continue

                if max_job_parallel > 1:
                    futures.append(
                        executor.submit(
                            self.execute_job,
                            job=job,
                            params=context,
                            result=result,
                            event=event,
                        ),
                    )
                    job_queue.task_done()
                    continue

                if len(futures) < 1:
                    futures.append(
                        executor.submit(
                            self.execute_job,
                            job=job,
                            params=context,
                            result=result,
                            event=event,
                        )
                    )
                    time.sleep(0.025)
                elif (future := futures.pop(0)).done() or future.cancelled():
                    job_queue.put(job_id)
                elif future.running() or "state=pending" in str(future):
                    time.sleep(0.075)
                    futures.insert(0, future)
                    job_queue.put(job_id)
                else:  # pragma: no cov
                    job_queue.put(job_id)
                    futures.insert(0, future)
                    time.sleep(0.025)
                    result.trace.warning(
                        f"[WORKFLOW]: ... Execution non-threading not "
                        f"handle: {future}."
                    )

                job_queue.task_done()

            if not_timeout_flag:
                job_queue.join()
                for future in as_completed(futures):
                    future.result()
                return result.catch(
                    status=FAILED if "errors" in result.context else SUCCESS,
                    context=context,
                )

            result.trace.error(f"[WORKFLOW]: {self.name!r} was timeout.")
            event.set()
            for future in futures:
                future.cancel()

        return result.catch(
            status=FAILED,
            context={
                "errors": WorkflowException(
                    f"{self.name!r} was timeout."
                ).to_dict()
            },
        )


class WorkflowPoke(Workflow):
    """Workflow Poke model that was implemented the poke method."""

    def queue(
        self,
        offset: float,
        end_date: datetime,
        queue: ReleaseQueue,
        audit: type[Audit],
        *,
        force_run: bool = False,
    ) -> ReleaseQueue:
        """Generate Release from all on values from the on field and store them
        to the ReleaseQueue object.

        :param offset: An offset in second unit for time travel.
        :param end_date: An end datetime object.
        :param queue: A workflow queue object.
        :param audit: An audit class that want to make audit object.
        :param force_run: A flag that allow to release workflow if the audit
            with that release was pointed.

        :rtype: ReleaseQueue
        """
        for on in self.on:

            queue.gen(
                end_date,
                audit,
                on.next(get_dt_now(offset=offset).replace(microsecond=0)),
                self.name,
                force_run=force_run,
            )

        return queue

    def poke(
        self,
        params: Optional[DictData] = None,
        start_date: Optional[datetime] = None,
        *,
        run_id: Optional[str] = None,
        periods: int = 1,
        audit: Optional[Audit] = None,
        force_run: bool = False,
        timeout: int = 1800,
        max_poking_pool_worker: int = 2,
    ) -> Result:
        """Poke workflow with a start datetime value that will pass to its
        `on` field on the threading executor pool for execute the `release`
        method (It run all schedules that was set on the `on` values).

            This method will observe its `on` field that nearing to run with the
        `self.release()` method.

            The limitation of this method is not allow run a date that gather
        than the current date.

        :param params: (DictData) A parameter data.
        :param start_date: (datetime) A start datetime object.
        :param run_id: (str) A workflow running ID for this poke.
        :param periods: (int) A periods in minutes value that use to run this
            poking. (Default is 1)
        :param audit: (Audit) An audit object that want to use on this poking
            process.
        :param force_run: (bool) A flag that allow to release workflow if the
            audit with that release was pointed. (Default is False)
        :param timeout: (int) A second value for timeout while waiting all
            futures run completely.
        :param max_poking_pool_worker: (int) The maximum poking pool worker.
            (Default is 2 workers)

        :raise WorkflowException: If the periods parameter less or equal than 0.

        :rtype: Result
        :return: A list of all results that return from `self.release` method.
        """
        audit: type[Audit] = audit or get_audit(extras=self.extras)
        result: Result = Result(
            run_id=(run_id or gen_id(self.name, unique=True))
        )

        # VALIDATE: Check the periods value should gather than 0.
        if periods <= 0:
            raise WorkflowException(
                "The period of poking should be `int` and grater or equal "
                "than 1."
            )

        if len(self.on) == 0:
            result.trace.warning(
                f"[POKING]: {self.name!r} not have any schedule!!!"
            )
            return result.catch(status=SUCCESS, context={"outputs": []})

        # NOTE: Create the current date that change microsecond to 0
        current_date: datetime = datetime.now().replace(microsecond=0)

        if start_date is None:
            # NOTE: Force change start date if it gathers than the current date,
            #   or it does not pass to this method.
            start_date: datetime = current_date
            offset: float = 0
        elif start_date <= current_date:
            start_date = start_date.replace(microsecond=0)
            offset: float = (current_date - start_date).total_seconds()
        else:
            raise WorkflowException(
                f"The start datetime should less than or equal the current "
                f"datetime, {current_date:%Y-%m-%d %H:%M:%S}."
            )

        # NOTE: The end date is using to stop generate queue with an input
        #   periods value. It will change to MM:59.
        #   For example:
        #       (input)  start_date = 12:04:12, offset = 2
        #       (output) end_date = 12:06:59
        end_date: datetime = start_date.replace(second=0) + timedelta(
            minutes=periods + 1, seconds=-1
        )

        result.trace.info(
            f"[POKING]: Execute Poking: {self.name!r} "
            f"({start_date:%Y-%m-%d %H:%M:%S} ==> {end_date:%Y-%m-%d %H:%M:%S})"
        )

        params: DictData = {} if params is None else params
        context: list[Result] = []
        q: ReleaseQueue = ReleaseQueue()

        # NOTE: Create reusable partial function and add Release to the release
        #   queue object.
        partial_queue = partial(
            self.queue, offset, end_date, audit=audit, force_run=force_run
        )
        partial_queue(q)
        if not q.is_queued:
            result.trace.warning(
                f"[POKING]: Skip {self.name!r}, not have any queue!!!"
            )
            return result.catch(status=SUCCESS, context={"outputs": []})

        with ThreadPoolExecutor(
            max_workers=dynamic(
                "max_poking_pool_worker",
                f=max_poking_pool_worker,
                extras=self.extras,
            ),
            thread_name_prefix="wf_poking_",
        ) as executor:

            futures: list[Future] = []

            while q.is_queued:

                # NOTE: Pop the latest Release object from the release queue.
                release: Release = heappop(q.queue)

                if reach_next_minute(release.date, offset=offset):
                    result.trace.debug(
                        f"[POKING]: Skip Release: "
                        f"{release.date:%Y-%m-%d %H:%M:%S}"
                    )
                    heappush(q.queue, release)
                    wait_until_next_minute(get_dt_now(offset=offset))

                    # WARNING: I already call queue poking again because issue
                    #   about the every minute crontab.
                    partial_queue(q)
                    continue

                heappush(q.running, release)
                futures.append(
                    executor.submit(
                        self.release,
                        release=release,
                        params=params,
                        audit=audit,
                        queue=q,
                        parent_run_id=result.run_id,
                    )
                )

                partial_queue(q)

            # WARNING: This poking method does not allow to use fail-fast
            #   logic to catching parallel execution result.
            for future in as_completed(futures, timeout=timeout):
                context.append(future.result())

        return result.catch(
            status=SUCCESS,
            context={"outputs": context},
        )


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class WorkflowTask:
    """Workflow task Pydantic dataclass object that use to keep mapping data and
    workflow model for passing to the multithreading task.

        This dataclass object is mapping 1-to-1 with workflow and cron runner
    objects.

        This dataclass has the release method for itself that prepare necessary
    arguments before passing to the parent release method.

    :param alias: (str) An alias name of Workflow model.
    :param workflow: (Workflow) A Workflow model instance.
    :param runner: (CronRunner)
    :param values: A value data that want to parameterize.
    :param extras: An extra parameter that use to override core config values.
    """

    alias: str
    workflow: Workflow
    runner: CronRunner
    values: DictData = field(default_factory=dict)
    extras: DictData = field(default_factory=dict)

    def release(
        self,
        release: Optional[Union[Release, datetime]] = None,
        run_id: Optional[str] = None,
        audit: type[Audit] = None,
        queue: Optional[ReleaseQueue] = None,
    ) -> Result:
        """Release the workflow task that passing an override parameter to
        the parent release method with the `values` field.

            This method can handler not passing release value by default
        generate step. It uses the `runner` field for generate release object.

        :param release: A release datetime or Release object.
        :param run_id: A workflow running ID for this release.
        :param audit: An audit class that want to save the execution result.
        :param queue: A ReleaseQueue object that use to mark complete.

        :raise ValueError: If a queue parameter does not pass while release
            is None.
        :raise TypeError: If a queue parameter does not match with ReleaseQueue
            type.

        :rtype: Result
        """
        audit: type[Audit] = audit or get_audit(extras=self.extras)

        if release is None:

            if queue is None:
                raise ValueError(
                    "If pass None release value, you should to pass the queue"
                    "for generate this release."
                )
            elif not isinstance(queue, ReleaseQueue):
                raise TypeError(
                    "The queue argument should be ReleaseQueue object only."
                )

            if queue.check_queue(self.runner.date):
                release = self.runner.next

                while queue.check_queue(release):
                    release = self.runner.next
            else:
                release = self.runner.date

        return self.workflow.release(
            release=release,
            params=self.values,
            run_id=run_id,
            audit=audit,
            queue=queue,
            override_log_name=self.alias,
        )

    def queue(
        self,
        end_date: datetime,
        queue: ReleaseQueue,
        audit: type[Audit],
        *,
        force_run: bool = False,
    ) -> ReleaseQueue:
        """Generate Release from the runner field and store it to the
        ReleaseQueue object.

        :param end_date: An end datetime object.
        :param queue: A workflow queue object.
        :param audit: An audit class that want to make audit object.
        :param force_run: (bool) A flag that allow to release workflow if the
            audit with that release was pointed.

        :rtype: ReleaseQueue
        """
        return queue.gen(
            end_date,
            audit,
            self.runner,
            self.alias,
            force_run=force_run,
            extras=self.extras,
        )

    def __repr__(self) -> str:
        """Override the `__repr__` method.

        :rtype: str
        """
        return (
            f"{self.__class__.__name__}(alias={self.alias!r}, "
            f"workflow={self.workflow.name!r}, runner={self.runner!r}, "
            f"values={self.values})"
        )

    def __eq__(self, other: WorkflowTask) -> bool:
        """Override the equal property that will compare only the same type.

        :rtype: bool
        """
        if isinstance(other, WorkflowTask):
            return (
                self.workflow.name == other.workflow.name
                and self.runner.cron == other.runner.cron
            )
        return NotImplemented
