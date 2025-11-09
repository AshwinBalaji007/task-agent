import logging
from typing import List
from rich import print as rprint
from rich.table import Table
from rich.console import Console

# --- Core Application Imports ---
from src.agent.main_agent import task_agent
from src.storage.vector_store import task_store
from src.models.task import Task
from src.core.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)
console = Console() 


def display_tasks(tasks: List[Task]):
    """Renders a list of tasks in a beautiful table using Rich."""
    table = Table(title="🧾 Current Tasks")

    table.add_column("ID", style="dim", width=4)
    table.add_column("Title", style="cyan", no_wrap=True)
    table.add_column("Priority", style="magenta")
    table.add_column("Category", style="green")
    table.add_column("Due Date", style="yellow")
    
    
    sorted_tasks = sorted(tasks, key=lambda t: t.created_at)

    for i, task in enumerate(sorted_tasks, 1):
        status_icon = "✅" if task.is_completed else ""
        due_date_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else ""
        table.add_row(
            str(i),
            f"{status_icon} {task.title}",
            task.priority,
            task.category,
            due_date_str
        )
    
    rprint(table)


def main_cli():
    """
    Main function to run the polished command-line interface.
    """
    rprint("🧠 [bold green]Welcome to the AI Task Manager Agent![/bold green]")
    rprint("Type 'list' to see tasks, 'exit' to quit, or enter a new one.")

    
    initial_tasks = task_store.list_tasks()
    if initial_tasks:
        display_tasks(initial_tasks)

    while True:
        try:
            user_input = console.input("> ")

            if user_input.lower() in ['exit', 'quit']:
                rprint("👋 [bold]Goodbye![/bold]")
                break
            
            if user_input.lower() == 'list':
                all_tasks = task_store.list_tasks()
                display_tasks(all_tasks)
                continue
            
            if not user_input.strip():
                continue
            
            # --- Main Agent Logic ---
            with console.status("[bold yellow]📨 Processing your query...[/bold yellow]", spinner="dots"):
                created_task: Task = task_agent.create_task_from_text(user_input)

            # Check for duplicates using the database as the source of truth
            if task_store.task_exists_by_title(created_task.title):
                rprint(f"⚠️  [bold yellow]Task '{created_task.title}' already exists — skipping duplicate.[/bold yellow]")
                continue
            
            # If new, add it to the database
            task_store.add_task(created_task)
            
            rprint(f"✨ [bold green]Task '{created_task.title}' was successfully created and saved![/bold green]")

            # Refresh the full list to show the new task
            all_tasks = task_store.list_tasks()
            display_tasks(all_tasks)

        except (ValueError, TypeError) as e:
            logger.error(f"Handled error: {e}", exc_info=True)
            rprint(f"❌ [bold red]Error: Could not process the task. Please try rephrasing.[/bold red]")
        except KeyboardInterrupt:
            rprint("\n👋 [bold]Goodbye![/bold]")
            break
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
            rprint(f"💥 [bold red]An unexpected system error occurred. See logs for details.[/bold red]")

if __name__ == "__main__":
    main_cli()