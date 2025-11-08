import logging
import sys
from src.core.config import settings

def setup_logging():
    """
    Configures the root logger for the application.

    This setup directs logs to the console with a specific format and sets
    the logging level based on the configuration in settings.yaml.

    In a real production app, this could be extended to log to files,
    services like Datadog, or other monitoring tools.
    """
    # Use the log level from our central settings
    log_level = settings.log_level.upper()
    
    # Create a basic configuration
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout  # Log to standard out
    )
    
    # Example usage in any other file:
    #
    # import logging
    # logger = logging.getLogger(__name__)
    # logger.info("This is an info message.")
    # logger.debug("This is a debug message.")
    #
    # To use, call setup_logging() once at the start of your main.py.

# You can call this function at the very beginning of src/main.py
# for a demonstration of its effect.