import chromadb
# --- THIS IS THE FIX ---
# We import the correct ABSTRACT TYPE for the client, not the factory function.
from chromadb.api import ClientAPI
# ---------------------
from typing import List, Dict, Any, cast
from src.models.task import Task
from src.storage.base_store import BaseTaskStore

class ChromaTaskStore(BaseTaskStore):
    """
    A task storage implementation using ChromaDB, designed for testability.
    """
    # And now we use the correct type in the __init__ method.
    def __init__(self, client: ClientAPI):
        """
        Initializes the store with a provided ChromaDB client.
        """
        self._client = client
        self._collection = self._client.get_or_create_collection(name="tasks")

    @classmethod
    def for_production(cls, path: str = "./chroma_db") -> "ChromaTaskStore":
        """Factory method to create a store with a persistent on-disk client."""
        client = chromadb.PersistentClient(path=path)
        return cls(client=client)

    @classmethod
    def for_testing(cls) -> "ChromaTaskStore":
        """Factory method to create a store with an in-memory client."""
        client = chromadb.EphemeralClient()
        return cls(client=client)

    # ... (all other methods remain exactly the same) ...
    def _task_to_metadata(self, task: Task) -> Dict[str, Any]:
        metadata = task.model_dump(exclude_none=True)
        for key, value in metadata.items():
            if hasattr(value, 'isoformat'): metadata[key] = value.isoformat()
        return metadata

    def _metadata_to_task(self, metadata: Dict[str, Any]) -> Task:
        return Task.model_validate(metadata)

    def add_task(self, task: Task):
        self._collection.add(
            ids=[task.id],
            documents=[task.title + " " + (task.description or "")],
            metadatas=[self._task_to_metadata(task)]
        )
        print(f"Task '{task.title}' added to ChromaDB.")

    def get_task(self, task_id: str) -> Task | None:
        result = self._collection.get(ids=[task_id])
        metadatas_list = result.get('metadatas')
        if not metadatas_list: return None
        first_metadata = metadatas_list[0]
        if first_metadata: return self._metadata_to_task(cast(Dict[str, Any], first_metadata))
        return None

    def list_tasks(self) -> List[Task]:
        results = self._collection.get()
        tasks: List[Task] = []
        metadatas_list = results.get('metadatas')
        if not metadatas_list: return []
        for meta in metadatas_list:
            if meta is not None: tasks.append(self._metadata_to_task(cast(Dict[str, Any], meta)))
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)

# The singleton uses the clean factory method.
task_store = ChromaTaskStore.for_production()