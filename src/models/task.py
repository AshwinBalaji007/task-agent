import uuid
from datetime import datetime, timezone
from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict

# These type aliases remain the same
TaskCategory = Literal["Work", "Personal", "Study", "Fitness", "Other"]
TaskPriority = Literal["Low", "Medium", "High", "Urgent"]


# NEW: The schema for the LLM's output.
# This only contains fields the LLM should generate, preventing it from
# trying to create internal fields like 'id' or 'created_at'.
class LLMTaskSchema(BaseModel):
    """
    Defines the schema of the data we expect the LLM to generate.
    It is a subset of the full Task model, excluding application-controlled fields.
    """
    title: str = Field(..., description="The main title of the task")
    category: TaskCategory = Field(default="Other", description="The category of the task")
    priority: TaskPriority = Field(default="Medium", description="The priority level of the task")
    description: Optional[str] = Field(None, description="A more detailed description of the task")
    due_date: Optional[datetime] = Field(None, description="The due date for the task")


# This is our complete, internal data model. It remains the same.
class Task(BaseModel):
    """
    Represents a full, structured task within our application.
    """
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "c7a8b9e1-0f2g-3h4i-5j6k-7l8m9n0o1p2q",
                "title": "Submit the ML Engineer assignment",
                "category": "Work",
                "priority": "Urgent",
                "description": "Complete the AI-Based Task Manager Agent project and record a video walkthrough.",
                "due_date": "2025-11-11T23:59:59Z",
                "created_at": "2025-11-08T17:00:00Z",
                "is_completed": False
            }
        }
    )
    
    # Application-controlled fields
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for the task")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="The timestamp when the task was created")
    is_completed: bool = Field(default=False, description="Whether the task is completed")

    # LLM-generated fields (inherited via the upgrade process)
    title: str = Field(..., description="The main title of the task")
    category: TaskCategory = Field(default="Other", description="The category of the task")
    priority: TaskPriority = Field(default="Medium", description="The priority level of the task")
    description: Optional[str] = Field(None, description="A more detailed description of the task")
    due_date: Optional[datetime] = Field(None, description="The due date for the task")