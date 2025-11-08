from collections import deque
from src.models.task import Task

class ShortTermMemory:
    """A simple in-memory store for the agent's recent history."""
    def __init__(self, max_size: int = 5):
        self.history = deque(maxlen=max_size)

    def add_task(self, task: Task):
        """Adds a new task's title to the recent history."""
        self.history.append(task.title.lower().strip())
        print(f"[Memory] Added '{task.title}' to history. Current history: {list(self.history)}")

    def was_recently_created(self, task_title: str) -> bool:
        """Checks if a task with the exact same title was recently created."""
        return task_title.lower().strip() in self.history

# --- Singleton instance ---
short_term_memory = ShortTermMemory()