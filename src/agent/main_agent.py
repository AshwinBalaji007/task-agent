import re
from datetime import datetime, timezone

from src.llm.client import llm_client
from src.agent.prompt_templates import task_creation_prompt, pydantic_parser
from src.models.task import Task, LLMTaskSchema 

def sanitize_and_extract_json(llm_output: str) -> str:
    """
    (Moved from task_parser.py)
    Finds and extracts the first valid JSON block from a raw LLM output string.
    """
    match = re.search(r"\{.*\}", llm_output, re.DOTALL)
    if match:
        return match.group(0)
    else:
        raise ValueError("No valid JSON object found in the LLM output.")

class TaskManagerAgent:
    """
    The main agent responsible for understanding natural language and creating tasks.
    It now handles the entire parsing and validation process.
    """
    def __init__(self):
        self.chain = task_creation_prompt | llm_client

    def create_task_from_text(self, user_query: str) -> Task:
        """
        Takes a natural language query, gets a response from the LLM, sanitizes
        and parses it, and returns a full, validated Task object.
        """
        print(f"Processing query: '{user_query}'...")

        prompt_inputs = {
            "query": user_query,
            "current_date": datetime.now(timezone.utc).isoformat()
        }
        
        llm_response = self.chain.invoke(prompt_inputs)
        raw_llm_output = llm_response.content
        
        if not isinstance(raw_llm_output, str):
            raise TypeError(f"Expected a string from LLM, but got {type(raw_llm_output)}")
        
        print(f"Raw LLM Output:\n{raw_llm_output}")

        try:
            # Sanitize the output to extract ONLY the JSON part.
            clean_json_str = sanitize_and_extract_json(raw_llm_output)

            # Parse the clean string into the simpler LLMTaskSchema.
            parsed_llm_data = pydantic_parser.parse(clean_json_str)

            # Create the final, complete Task object.
            final_task = Task(**parsed_llm_data.model_dump())
            
            print(f"Successfully parsed task: {final_task.title}")
            return final_task
        except Exception as e:
            print(f"Agent failed to create task: {e}")
            raise ValueError(f"Failed to create task from LLM output. Error: {e}")

# --- Singleton instance ---
task_agent = TaskManagerAgent()