import os
from langchain_google_genai import ChatGoogleGenerativeAI
from src.core.config import settings

def get_llm_client() -> ChatGoogleGenerativeAI:
    """
    Initializes and returns the LangChain client for the Google Gemini model.

    This function configures the client using settings from our centralized
    configuration system, including the model name and the API key.

    Returns:
        An instance of ChatGoogleGenerativeAI configured and ready to use.
    """
    # LangChain's Google provider automatically looks for the GOOGLE_API_KEY
    # environment variable. Our config system ensures it's loaded.
    # We will also pass our other configurations.
    
    # Ensure the environment variable is set for the LangChain library to pick it up.
    # While our Settings class validates it, some libraries might read directly from os.environ.
    # This is a good defensive practice.
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = settings.google_api_key

    llm = ChatGoogleGenerativeAI(
        model=settings.llm.model_name,
        temperature=settings.llm.temperature,
    )
    
    return llm

# --- Singleton instance ---
# Create one instance of the client to be reused across the application.
# This avoids re-initializing the client on every call, which is inefficient.
llm_client = get_llm_client()

# You can test this file directly to see if the client initializes correctly.
# Run `python -m src.llm.client` from the root directory.
# If it runs without error, your API key and setup are correct.
if __name__ == "__main__":
    print("LLM client initialized successfully!")
    print(f"Model: {llm_client.model}")
    print(f"Temperature: {llm_client.temperature}")
    
    # Example invocation:
    # from langchain_core.messages import HumanMessage
    # response = llm_client.invoke([HumanMessage(content="Hello! Tell me a joke.")])
    # print(response.content)