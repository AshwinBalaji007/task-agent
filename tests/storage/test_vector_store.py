import pytest
import os
import shutil
from collections.abc import Iterator # <-- IMPORT Iterator FOR CORRECT TYPE HINTING

from src.storage.vector_store import ChromaTaskStore
from src.models.task import Task

TEST_DB_PATH = "./test_chroma_db"

@pytest.fixture
def temp_chroma_store() -> Iterator[ChromaTaskStore]: # <-- FIX: Use Iterator for the generator's return type
    """
    Pytest fixture to create a temporary ChromaTaskStore for testing.
    This ensures tests are isolated and don't interfere with each other or
    the main database. It is automatically cleaned up after the test runs.
    """
    if os.path.exists(TEST_DB_PATH):
        shutil.rmtree(TEST_DB_PATH)
    
    store = ChromaTaskStore(path=TEST_DB_PATH)
    yield store
    
    if os.path.exists(TEST_DB_PATH):
        shutil.rmtree(TEST_DB_PATH)


def test_add_and_get_task(temp_chroma_store: ChromaTaskStore):
    """
    Tests the basic add and retrieve functionality of the task store.
    """
    # 1. Create a new task (explicitly pass None to satisfy the linter)
    new_task = Task(
        title="Test Task",
        category="Work",
        priority="High",
        description=None, # <-- FIX: Be explicit for clarity and to satisfy Pylance
        due_date=None     # <-- FIX: Be explicit for clarity and to satisfy Pylance
    )
    
    # 2. Add it to the store
    temp_chroma_store.add_task(new_task)
    
    # 3. Retrieve it by its ID
    retrieved_task = temp_chroma_store.get_task(new_task.id)
    
    # 4. Assert that the retrieved task is correct
    assert retrieved_task is not None
    assert retrieved_task.id == new_task.id
    assert retrieved_task.title == "Test Task"
    assert retrieved_task.priority == "High"

def test_list_tasks(temp_chroma_store: ChromaTaskStore):
    """
    Tests the listing functionality of the task store.
    """
    # FIX: Be explicit for clarity and to satisfy Pylance
    task1 = Task(title="Task 1", description=None, due_date=None)
    task2 = Task(title="Task 2", description=None, due_date=None)
    
    temp_chroma_store.add_task(task1)
    temp_chroma_store.add_task(task2)
    
    all_tasks = temp_chroma_store.list_tasks()
    
    assert len(all_tasks) == 2
    task_titles = {t.title for t in all_tasks}
    assert "Task 1" in task_titles
    assert "Task 2" in task_titles