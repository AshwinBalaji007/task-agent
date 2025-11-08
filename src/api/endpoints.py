# To run this API:
# 1. Ensure you are in your activated virtual environment.
# 2. Run from the project root: `uvicorn src.api.endpoints:app --reload`
# 3. Access the interactive documentation at http://127.0.0.1:8000/docs

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.agent.main_agent import task_agent
from src.storage.vector_store import task_store
from src.models.task import Task

app = FastAPI(
    title="AI Task Manager Agent API",
    description="An API to interact with the AI agent to create and manage tasks.",
    version="0.1.0"
)

# Pydantic model for the request body to create a task
class CreateTaskRequest(BaseModel):
    query: str

@app.post("/task/create", response_model=Task)
async def create_task(request: CreateTaskRequest):
    """
    Accepts a natural language query and uses the AI agent to create
    a structured task, then saves it to the vector store.
    """
    try:
        task = task_agent.create_task_from_text(request.query)
        task_store.add_task(task)
        return task
    except (ValueError, TypeError) as e:
        raise HTTPException(status_code=400, detail=f"Failed to process task: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@app.get("/tasks", response_model=list[Task])
async def list_tasks():
    """
    Retrieves and lists all tasks currently in the vector store.
    """
    return task_store.list_tasks()