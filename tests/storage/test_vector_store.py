import pytest
from collections.abc import Iterator
import chromadb

from src.storage.vector_store import ChromaTaskStore
from src.models.task import Task

@pytest.fixture
def in_memory_chroma_store() -> Iterator[ChromaTaskStore]:
    """
    Pytest fixture that creates an isolated, in-memory ChromaTaskStore for each test.
    """
    ephemeral_client = chromadb.EphemeralClient()
    store = ChromaTaskStore(client=ephemeral_client)
    yield store
    ephemeral_client.reset()

def test_add_and_get_task(in_memory_chroma_store: ChromaTaskStore):
    """Tests the basic add and retrieve functionality."""
    # Be explicit with optional arguments to satisfy the Pylance linter.
    new_task = Task(title="Test Task", category="Work", priority="High", description=None, due_date=None)
    
    in_memory_chroma_store.add_task(new_task)
    retrieved_task = in_memory_chroma_store.get_task(new_task.id)
    
    assert retrieved_task is not None
    assert retrieved_task.id == new_task.id
    assert retrieved_task.title == "Test Task"

def test_list_tasks(in_memory_chroma_store: ChromaTaskStore):
    """Tests the listing functionality in a clean environment."""
    assert len(in_memory_chroma_store.list_tasks()) == 0
    
    # Be explicit with optional arguments to satisfy the Pylance linter.
    task1 = Task(title="Task 1", description=None, due_date=None)
    task2 = Task(title="Task 2", description=None, due_date=None)
    
    in_memory_chroma_store.add_task(task1)
    in_memory_chroma_store.add_task(task2)
    
    all_tasks = in_memory_chroma_store.list_tasks()
    
    assert len(all_tasks) == 2
    task_titles = {t.title for t in all_tasks}
    assert "Task 1" in task_titles
    assert "Task 2" in task_titles