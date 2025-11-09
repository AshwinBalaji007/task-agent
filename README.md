# AI Task Manager Agent

[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![Google AI](https://img.shields.io/badge/Google%20AI-Gemini-blueviolet)](https://ai.google.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![CI Status](https://github.com/AshwinBalaji007/task-agent/actions/workflows/main.yml/badge.svg)](https://github.com/AshwinBalaji007/task-agent/actions/workflows/main.yml)

An AI-powered agent that accepts natural language input for tasks, intelligently categorizes and prioritizes them, and stores them in a persistent vector database. This project is built with a focus on production-ready code, professional engineering practices, and a scalable agentic architecture.

---

### Features

-   **Natural Language Understanding:** Leverages Google's Gemini LLM via LangChain to parse complex user requests into structured data.
-   **Structured Data Extraction:** Converts unstructured text into a validated Pydantic data model (`Task`), reliably identifying titles, categories, priorities, and due dates.
-   **Persistent Vector Storage:** Uses ChromaDB to store tasks, enabling both data persistence and future semantic search capabilities.
-   **Real-time Duplicate Detection:** Employs an efficient metadata filter on the database to prevent duplicate tasks from being created, ensuring data integrity.
-   **User-Friendly CLI:** A well-formatted and interactive command-line interface built with the `rich` library for clear tables, status indicators, and user feedback.
-   **Ready for Deployment:**
    -   **API Included:** A ready-to-use FastAPI server (`/src/api`) is provided to expose the agent's functionality as a scalable web service.
    -   **Containerized:** A `Dockerfile` is included for easy, reproducible deployment in any environment.
-   **Fully Tested & Verified:** The project includes a comprehensive test suite using `pytest` for unit testing and a CI/CD pipeline using GitHub Actions to automatically verify code quality and stability on every push.

---

### System Design & Architecture

The system is designed with a modular, decoupled architecture to ensure scalability and maintainability.

![Architecture Diagram](docs/architecture_diagram.png)

1.  **Interface (CLI/API):** The user interacts with the system through the command-line interface (`src/main.py`) or a scalable FastAPI server (`src/api/endpoints.py`).
2.  **Agent Core (`src/agent/main_agent.py`):** The central orchestrator that receives the user query and manages the processing workflow.
3.  **Prompt Engineering (`src/agent/prompt_templates.py`):** The agent formats a detailed prompt, providing the LLM with context, instructions, and a specific output schema (`LLMTaskSchema`). This is a crucial step to ensure reliable and predictable output.
4.  **LLM Interaction (`src/llm/client.py`):** The formatted prompt is sent to the Google Gemini LLM via a dedicated client.
5.  **Parsing & Sanitization:** The agent receives the raw output from the LLM. It first sanitizes the text to remove any non-JSON formatting (e.g., Markdown) and then parses the clean string into a safe, intermediate data schema (`LLMTaskSchema`).
6.  **Data Validation & Enrichment:** The sanitized data is used to create the final `Task` object for use within the application. At this stage, application-controlled fields (e.g., `id`, `created_at`) are generated, keeping LLM and application concerns cleanly separated.
7.  **Database Interaction (`src/storage/vector_store.py`):** The final, validated `Task` object is saved to the persistent ChromaDB vector store. The store is also queried for duplicate checks before saving new entries.

---

### Tech Stack

-   **AI & Machine Learning:** LangChain, Google Gemini API, Sentence Transformers
-   **Vector Database:** ChromaDB (for the main application), FAISS (for notebook demonstrations)
-   **API Framework:** FastAPI, Uvicorn
-   **CLI & UI:** Rich
-   **Data Validation:** Pydantic
-   **Testing & CI/CD:** Pytest, GitHub Actions
-   **Containerization:** Docker

---

### Getting Started

Follow these steps to set up and run the project locally.

#### 1. Clone the Repository

```bash
git clone https://github.com/AshwinBalaji007/task-agent.git
cd task-agent
```

#### 2. Create and Activate a Virtual Environment

```bash
# For Unix/macOS
python3 -m venv .venv
source .venv/bin/activate

# For Windows
python -m venv .venv
.\.venv\Scripts\activate
```

#### 3. Install Dependencies

Install all required Python libraries from the requirements file.

```bash
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables

A Google API key is required to use the Gemini model.

1.  Create a `.env` file from the provided template:
    ```bash
    cp .env.example .env
    ```
2.  Open the `.env` file and add your Google API key, which can be obtained from [Google AI Studio](https://makersuite.google.com/).
    ```ini
    GOOGLE_API_KEY="your_google_api_key_here"
    ```

#### 5. (Optional) Seed the Database

To populate the database with sample data for demonstration, run the seed script:

```bash
python -m scripts.seed_database
```

---

### Usage

The agent can be run via the CLI, as an API server, or be validated by running the test suite.

#### Run the Command-Line Interface

This is the primary entry point for interacting with the agent.

```bash
python -m src.main
```
Once running, you can use commands such as `list`, `help`, `exit`, or simply type a task to add it.

#### Run the API Server

The project includes a fully functional FastAPI server for programmatic access.

```bash
uvicorn src.api.endpoints:app --reload
```
Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

#### Run the Test Suite

To verify that all components are working correctly, run the `pytest` suite:

```bash
python -m pytest
```

---

### Project Structure

The project is organized with a clean, scalable structure suitable for production environments:

```
├── .github/      # CI/CD workflows for GitHub Actions
├── configs/      # YAML configuration files (e.g., model settings)
├── docs/         # System design documentation and diagrams
├── notebooks/    # Jupyter notebooks for experimentation and proof-of-concepts
├── scripts/      # Utility scripts (e.g., database seeding)
├── src/          # Main source code for the application
│   ├── agent/    # Core agent logic and prompt engineering
│   ├── api/      # FastAPI endpoints for the web service
│   ├── core/     # Core components like configuration and logging
│   ├── llm/      # LLM client setup and interaction
│   ├── models/   # Pydantic data models and schemas
│   └── storage/  # Database interaction and storage logic
└── tests/        # Test suite with pytest
```

---

### Video Walkthrough

**Link:** [Your Unlisted YouTube/Vimeo Link Here]
