import pytest
from src.agent.task_parser import parse_llm_output_to_task
from src.models.task import Task

def test_parse_valid_json_to_task():
    """
    Tests if a valid JSON string from the LLM is correctly parsed into a Task object.
    """
    llm_output = """
    {
      "title": "Test the parser",
      "category": "Work",
      "priority": "High",
      "description": "This is a test description.",
      "due_date": "2025-12-01T12:00:00Z"
    }
    """
    task = parse_llm_output_to_task(llm_output)
    
    assert isinstance(task, Task)
    assert task.title == "Test the parser"
    assert task.priority == "High"
    assert task.category == "Work"

def test_parse_invalid_json_raises_error():
    """
    Tests if malformed JSON correctly raises a ValueError.
    """
    llm_output = '{"title": "Incomplete JSON"'
    
    with pytest.raises(ValueError, match="Failed to parse LLM output"):
        parse_llm_output_to_task(llm_output)