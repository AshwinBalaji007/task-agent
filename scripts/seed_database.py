import sys
from datetime import datetime, timedelta, timezone  # <-- IMPORT timezone

# Ensure the main 'src' directory is in the Python path.
sys.path.append('.')

from src.models.task import Task
from src.storage.vector_store import task_store

def seed_database():
    """
    Populates the ChromaDB vector store with a predefined set of sample tasks.

    This script is idempotent; it checks if a task with the same title already exists
    to avoid creating duplicate entries if run multiple times.
    """
    print("--- Starting Database Seeding ---")
    
    # Use timezone.utc to make all datetimes timezone-aware
    now_utc = datetime.now(timezone.utc)

    sample_tasks = [
        Task(
            title="Finalize Q4 marketing report",
            category="Work",
            priority="High",
            description="Complete the data analysis and write the executive summary.",
            due_date=now_utc + timedelta(days=5) # <-- FIX: Use aware datetime
        ),
        Task(
            title="Schedule annual team offsite",
            category="Work",
            priority="Medium",
            description="Coordinate with HR and find a suitable venue for the first week of next month.",
            due_date=now_utc + timedelta(days=14) # <-- FIX: Use aware datetime
        ),
        Task(
            title="Buy groceries for the week",
            category="Personal",
            priority="Medium",
            description="Need milk, eggs, bread, avocados, and chicken breast.",
            due_date=None
        ),
        Task(
            title="Go for a 30-minute run",
            category="Fitness",
            priority="Low",
            description="Morning run in the park to stay active.",
            due_date=None
        ),
        Task(
            title="Study the new LangChain v1.0 documentation",
            category="Study",
            priority="High",
            description="Focus on the LCEL (LangChain Expression Language) changes.",
            due_date=None
        ),
    ]

    existing_tasks = task_store.list_tasks()
    existing_titles = {task.title.lower() for task in existing_tasks}
    
    tasks_added = 0
    for task in sample_tasks:
        if task.title.lower() not in existing_titles:
            task_store.add_task(task)
            print(f"  -> Added task: '{task.title}'")
            tasks_added += 1
        else:
            print(f"  -> Skipping existing task: '{task.title}'")
            
    print(f"\n--- Database Seeding Complete. Added {tasks_added} new tasks. ---")


if __name__ == "__main__":
    seed_database()