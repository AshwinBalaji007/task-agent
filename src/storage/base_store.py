from abc import ABC, abstractmethod
from typing import List
from src.models.task import Task

class BaseTaskStore(ABC):
    """Abstract base class for a task storage system."""

    @abstractmethod
    def add_task(self, task: Task) -> None:
        """Adds a new task to the store."""
        pass

    @abstractmethod
    def get_task(self, task_id: str) -> Task | None:
        """Retrieves a task by its ID."""
        pass

    @abstractmethod
    def list_tasks(self) -> List[Task]:
        """Lists all tasks in the store."""
        pass