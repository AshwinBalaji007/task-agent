import pytest
from collections.abc import Iterator
import chromadb
# --- THIS IS THE KEY ---
# We need to import the Settings class to configure our test client.
from chromadb.config import Settings

from src.storage.vector_store import ChromaTaskStore
from src.models.task import Task

@pytest.fixture
def in_memory_chroma_store() -> Iterator[ChromaTaskStore]:
    """
    Pytest fixture that creates an isolated, in-memory ChromaTaskStore for each test.
    
    It now creates a client with a special configuration that explicitly allows
    the `reset()` command, which is required for guaranteeing test isolation in
    strict CI environments.
    """
    # Setup: Create a settings object that allows database resets.
    settings = Settings(allow_reset=True)
    
    # Create the client using these specific settings.
    ephemeral_client = chromadb.EphemeralClient(settings=settings)
    
    store = ChromaTaskStore(client=ephemeral_client)
    
    yield store
    
    # Teardown: This command will now be authorized and will succeed.
    ephemeral_client.reset()


def test_add_and_get_task(in_memory_chroma_store: ChromaTaskStore):
    """Tests the basic add and retrieve functionality."""
    new_task = Task(title="Test Task", category="Work", priority="High", description=None, due_date=None)
    
    in_memory_chroma_store.add_task(new_task)
    retrieved_task = in_memory_chroma_store.get_task(new_task.id)
    
    assert retrieved_task is not None
    assert retrieved_task.id == new_task.id
    assert retrieved_task.title == "Test Task"

def test_list_tasks(in_memory_chroma_store: ChromaTaskStore):
    """Tests the listing functionality in a perfectly clean, isolated environment."""
    # This assertion will now pass because the teardown from the previous test worked.
    assert len(in_memory_chroma_store.list_tasks()) == 0
    
    task1 = Task(title="Task 1", description=None, due_date=None)
    task2 = Task(title="Task 2", description=None, due_date=None)
    
    in_memory_chroma_store.add_task(task1)
    in_memory_chroma_store.add_task(task2)
    
    all_tasks = in_memory_chroma_store.list_tasks()
    
    assert len(all_tasks) == 2
    task_titles = {t.title for t in all_tasks}
    assert "Task 1" in task_titles
    assert "Task 2" in task_titles