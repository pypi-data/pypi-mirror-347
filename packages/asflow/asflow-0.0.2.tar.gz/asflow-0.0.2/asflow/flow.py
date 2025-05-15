import asyncio
import contextlib
import contextvars
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from typing import Any, Callable

import rich
import rich.console
import rich.progress

from .task import Task


class Flow:
    run_var = contextvars.ContextVar("@flow")

    def __init__(
        self,
        base: str | Path = ".",
        stderr: bool = True,
        verbose: bool = False,
    ):
        self.base = Path(base)
        self.verbose = verbose
        self.console = rich.console.Console(stderr=stderr)
        self.task = Task(self)

    @property
    def run(self):
        try:
            return Flow.run_var.get()
        except LookupError:
            return None

    def path(self, filename):
        return self.base / filename

    def __call__(self, func=None, **kwargs):
        if "verbose" not in kwargs:
            kwargs["verbose"] = self.verbose

        if func is None:
            # @flow(**kwargs)
            return FlowConfig(self, **kwargs).decorator
        else:
            # @flow
            return FlowConfig(self, **kwargs).decorator(func)


@dataclass
class FlowConfig:
    flow: Flow
    progress: bool = True
    verbose: bool = False

    def decorator(self, func):
        assert asyncio.iscoroutinefunction(func)

        @wraps(func)
        async def async_flow_wrapper(*args, **kwargs):
            async with AsyncFlowRun(self, func, args, kwargs) as run:
                token = Flow.run_var.set(run)
                try:
                    return await func(*args, **kwargs)
                finally:
                    Flow.run_var.reset(token)

        return async_flow_wrapper


@dataclass
class TaskState:
    task_id: str
    total: int


@dataclass
class AsyncFlowRun:
    config: FlowConfig
    func: Callable
    args: list[Any]
    kwargs: dict[Any, Any]

    FLOW_FORMAT = "[blue]@flow[/] {flow}()"
    TASK_FORMAT = " [blue]@task[/] {task}()"
    TASKRUN_FORMAT = "       {desc}"

    async def __aenter__(self):
        self._stack = contextlib.ExitStack()

        if self.config.progress:
            progress = rich.progress.Progress(console=self.config.flow.console, transient=True)
            self.progress = self._stack.enter_context(progress)
            description = self.FLOW_FORMAT.format(flow=self.func.__name__)
            self.progress.add_task(description, start=False)
            self.running_tasks = {}
        else:
            self.progress = None

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return self._stack.__exit__(exc_type, exc_val, exc_tb)

    def add_task(self, task_run):
        if self.progress:
            func = task_run.func
            if state := self.running_tasks.get(func):
                state.total += 1
                self.progress.update(state.task_id, total=state.total)
            else:
                description = self.TASK_FORMAT.format(task=func.__name__)
                task_id = self.progress.add_task(description, total=1)
                self.running_tasks[func] = TaskState(task_id=task_id, total=1)

    def remove_task(self, task_run):
        if self.progress:
            func = task_run.func
            state = self.running_tasks[func]
            self.progress.advance(state.task_id)
