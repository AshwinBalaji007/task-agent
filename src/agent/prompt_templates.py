from datetime import datetime
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from src.models.task import LLMTaskSchema, TaskCategory, TaskPriority

pydantic_parser = PydanticOutputParser(pydantic_object=LLMTaskSchema)

task_creation_prompt = PromptTemplate(
    template="""
    You are an expert AI assistant that extracts structured information from user input.
    Your goal is to create a complete `Task` object based on the user's query.

    Analyze the user's query below and fill in all the fields of the Task object as accurately as possible.

    User Query:
    "{query}"

    Contextual Information:
    - Today's date is {current_date}. Use this to resolve relative dates like "tomorrow" or "next week".

    Follow these specific instructions:
    - Title: Create a concise and clear title for the task.
    - Category: Assign one of the following categories: {categories}. If no specific category fits, use "Other".
    - Priority: Assign a priority level: {priorities}. Infer this from words like "urgent," "ASAP," or if no urgency is implied, default to "Medium".
    - Due Date: If a date or time is mentioned, convert it to a valid ISO 8601 datetime format (YYYY-MM-DDTHH:MM:SSZ).
    - Description: If there are extra details in the query, add them here. Otherwise, leave it empty.

    {format_instructions}
    """,
    input_variables=["query", "current_date"],
    partial_variables={
        "format_instructions": pydantic_parser.get_format_instructions(),
        "categories": list(TaskCategory.__args__),
        "priorities": list(TaskPriority.__args__),
    },
)