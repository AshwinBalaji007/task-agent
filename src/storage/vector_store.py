import chromadb
from typing import List, Dict, Any, cast
from src.models.task import Task
from src.storage.base_store import BaseTaskStore

class ChromaTaskStore(BaseTaskStore):
    """
    A task storage implementation using ChromaDB as the vector store.
    This version includes robust type checking to prevent runtime errors.
    """
    def __init__(self, path: str = "./chroma_db"):
        client = chromadb.PersistentClient(path=path)
        self._collection = client.get_or_create_collection(name="tasks")

    def _task_to_metadata(self, task: Task) -> Dict[str, Any]:
        """Converts a Task object to a metadata dictionary for Chroma, excluding None values."""
        metadata = task.model_dump(exclude_none=True)
        # ChromaDB metadata values must be strings, ints, floats, or bools.
        # Convert datetime objects to ISO format strings.
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
        
        # Safely access the list of metadatas
        metadatas_list = result.get('metadatas')
        if not metadatas_list:
            return None
        
        # The list might not be empty, but its first element could be None
        first_metadata = metadatas_list[0]
        if first_metadata:
            # Cast the specific Metadata type to a generic Dict for our function
            return self._metadata_to_task(cast(Dict[str, Any], first_metadata))
            
        return None

    def list_tasks(self) -> List[Task]:
        """Retrieves all tasks from the collection with improved type safety."""
        results = self._collection.get()
        tasks: List[Task] = []
        
        # Safely access the list of metadatas
        metadatas_list = results.get('metadatas')
        if not metadatas_list:
            return []
        
        for meta in metadatas_list:
            if meta is not None:
                # Cast the specific Metadata type to a generic Dict for our function
                tasks.append(self._metadata_to_task(cast(Dict[str, Any], meta)))
        
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)

# --- Singleton instance ---
task_store = ChromaTaskStore()