import logging

from src.agent.main_agent import task_agent
from src.storage.vector_store import task_store
from src.models.task import Task
from src.core.logging_config import setup_logging
from src.memory.short_term_memory import short_term_memory

logger = logging.getLogger(__name__)

def display_tasks():
    # ... (This function remains unchanged)
    logger.info("\n--- Current Tasks ---")
    tasks = task_store.list_tasks()
    if not tasks:
        logger.info("No tasks found.")
    else:
        sorted_tasks = sorted(tasks, key=lambda t: t.created_at)
        for i, task in enumerate(sorted_tasks, 1):
            status = "✅" if task.is_completed else "🔳"
            due_date_str = task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else "No due date"
            logger.info(
                f"{i}. {status} {task.title} | P: {task.priority} | C: {task.category} | Due: {due_date_str}"
            )
    logger.info("---------------------\n")


def main_cli():
    """
    Main function with the corrected agent loop logic.
    """
    setup_logging()
    logger.info("Welcome to the AI Task Manager Agent!")
    logger.info("Type 'list' to see all tasks, 'exit' to quit, or enter a new task.")
    
    while True:
        try:
            user_input = input("> ").strip()
            
            if user_input.lower() == 'exit':
                logger.info("Goodbye!")
                break
            
            if user_input.lower() == 'list':
                display_tasks()
                continue
            
            if not user_input:
                continue
            
            # --- CORRECTED LOGIC FLOW ---
            
            # 1. ALWAYS parse the text first to understand the core task.
            created_task: Task = task_agent.create_task_from_text(user_input)
            
            # 2. NOW, check the PARSED TITLE against the memory.
            if short_term_memory.was_recently_created(created_task.title):
                logger.warning(f"Task '{created_task.title}' seems to be a duplicate of a recent one. Aborting.")
                continue  # Skip saving and updating memory
            
            # 3. If it's not a duplicate, save it to the database and memory.
            task_store.add_task(created_task)
            short_term_memory.add_task(created_task)

            logger.info(f"\n✨ Task '{created_task.title}' was successfully created and saved!")
            display_tasks()

        except ValueError as e:
            logger.error(f"Could not process the task. Please try rephrasing. Details: {e}")
        except KeyboardInterrupt:
            logger.info("\nGoodbye!")
            break
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main_cli()