import chromadb
from typing import List, Dict, Any, cast, Optional
from src.models.task import Task
from src.storage.base_store import BaseTaskStore

class ChromaTaskStore(BaseTaskStore):
    """
    A task storage implementation using ChromaDB.
    Supports both persistent (on-disk) and in-memory clients for flexibility.
    """
    def __init__(self, path: Optional[str] = "./chroma_db"):
        # This is a key change for testability:
        # If a path is provided, use a persistent client that writes to disk.
        # If the path is None, use an EphemeralClient for in-memory testing.
        if path:
            client = chromadb.PersistentClient(path=path)
        else:
            client = chromadb.EphemeralClient() # In-memory, no disk writes
        
        self._collection = client.get_or_create_collection(name="tasks")

    # ... (the rest of the file remains exactly the same) ...
    def _task_to_metadata(self, task: Task) -> Dict[str, Any]:
        """Converts a Task object to a metadata dictionary for Chroma, excluding None values."""
        metadata = task.model_dump(exclude_none=True)
        for key, value in metadata.items():
            if hasattr(value, 'isoformat'):
                metadata[key] = value.isoformat()
        return metadata

    def _metadata_to_task(self, metadata: Dict[str, Any]) -> Task:
        """Converts a metadata dictionary from Chroma back to a Task object."""
        return Task.model_validate(metadata)

    def add_task(self, task: Task):
        """Adds a single task to the ChromaDB collection."""
        self._collection.add(
            ids=[task.id],
            documents=[task.title + " " + (task.description or "")],
            metadatas=[self._task_to_metadata(task)]
        )
        print(f"Task '{task.title}' added to ChromaDB.")

    def get_task(self, task_id: str) -> Task | None:
        """Retrieves a task from ChromaDB by its ID with improved type safety."""
        result = self._collection.get(ids=[task_id])
        metadatas_list = result.get('metadatas')
        if not metadatas_list:
            return None
        
        first_metadata = metadatas_list[0]
        if first_metadata:
            return self._metadata_to_task(cast(Dict[str, Any], first_metadata))
        return None

    def list_tasks(self) -> List[Task]:
        """Retrieves all tasks from the collection with improved type safety."""
        results = self._collection.get()
        tasks: List[Task] = []
        metadatas_list = results.get('metadatas')
        if not metadatas_list:
            return []
        
        for meta in metadatas_list:
            if meta is not None:
                tasks.append(self._metadata_to_task(cast(Dict[str, Any], meta)))
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)


# The singleton for the main app still uses the default persistent client. Perfect.
task_store = ChromaTaskStore()