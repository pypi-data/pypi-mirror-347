from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from rich.progress import Progress, TaskID


class RunningProgress(ABC):
    @abstractmethod
    def update(self, advance: int = 1):
        pass

    @abstractmethod
    def finish(self):
        pass


class ProgressIndicator(ABC):
    @abstractmethod
    def start(self, message: str, duration: Optional[int] = None) -> RunningProgress:
        pass

    @staticmethod
    def create() -> ProgressIndicator:
        return RichProgressIndicator()


class RichProgressIndicator(ProgressIndicator):
    def __init__(self):
        self.progress = Progress()

    def start(self, message: str, duration: Optional[int] = None) -> RunningProgress:
        task = self.progress.add_task(message, total=duration)
        return RichRunningProgress(self.progress, task)


class RichRunningProgress(RunningProgress):
    def __init__(self, progress: Progress, task: TaskID):
        self.progress = progress
        self.task = task

    def update(self, advance: int = 1):
        self.progress.update(self.task, advance=advance)

    def finish(self):
        self.progress.stop()
