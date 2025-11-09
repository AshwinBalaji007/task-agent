# AI Task Manager Agent

[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![Google AI](https://img.shields.io/badge/Google%20AI-Gemini-blueviolet)](https://ai.google.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![CI Status](https://github.com/AshwinBalaji007/task-agent/actions/workflows/main.yml/badge.svg)](https://github.com/AshwinBalaji007/task-agent/actions/workflows/main.yml)

An AI-powered agent that takes natural language input for tasks, intelligently categorizes and prioritizes them, and stores them in a persistent vector database. This project is built with a focus on production-ready code, professional engineering practices, and a scalable agentic architecture.

---

### ✨ Features

*   **🧠 Natural Language Understanding:** Leverages Google's Gemini LLM via LangChain to parse complex user requests.
*   **🤖 Structured Data Extraction:** Intelligently converts unstructured text into a validated Pydantic data model (`Task`), identifying titles, categories, priorities, and due dates.
*   **💾 Persistent Vector Storage:** Uses ChromaDB to store tasks, enabling both persistence and future semantic search capabilities.
*   **🔍 Real-time Duplicate Detection:** Employs an efficient metadata filter on the database to prevent duplicate tasks from being created.
*   **💅 Polished CLI:** A beautiful and user-friendly command-line interface built with `rich` for formatted tables, status indicators, and clear feedback.
*   **🚀 Ready for Deployment:**
    *   **API Included:** A ready-to-use FastAPI server (`/src/api`) to expose the agent's functionality as a web service.
    *   **Containerized:** A `Dockerfile` is provided for easy, reproducible deployment in any environment.
*   **✅ Fully Tested & Verified:** The project includes a full test suite with `pytest` and a CI/CD pipeline using GitHub Actions to ensure code quality and stability.

---

### 🏛️ System Design & Architecture

The system is designed with a modular, decoupled architecture to ensure scalability and maintainability.

![Architecture Diagram](docs/architecture_diagram.png)

1.  **Interface (CLI/API):** The user interacts with the system through a polished command-line interface (`src/main.py`) or a scalable FastAPI server (`src/api/endpoints.py`).
2.  **Agent Core (`src/agent/main_agent.py`):** This orchestrator receives the user query.
3.  **Prompt Engineering (`src/agent/prompt_templates.py`):** The agent formats a detailed prompt, providing the LLM with context, instructions, and a specific output schema (`LLMTaskSchema`). This is a crucial step to ensure reliable output.
4.  **LLM Interaction (`src/llm/client.py`):** The formatted prompt is sent to the Gemini LLM.
5.  **Parsing & Sanitization:** The agent receives the raw LLM output. It sanitizes the text to remove Markdown formatting and then parses it into the safe `LLMTaskSchema`.
6.  **Data Validation & Enrichment:** The sanitized data is then used to create a full `Task` object. The application adds its own internal fields at this stage (e.g., `id`, `created_at`), keeping LLM and application concerns separate.
7.  **Database Interaction (`src/storage/vector_store.py`):** The final `Task` object is saved to the persistent ChromaDB vector store. The store is also used for duplicate checks before saving.

---

### 🛠️ Tech Stack

*   **AI & Machine Learning:** LangChain, Google Gemini API, Sentence Transformers
*   **Vector Database:** ChromaDB (for the main app), FAISS (for notebook demos)
*   **API Framework:** FastAPI, Uvicorn
*   **CLI & UI:** Rich
*   **Data Validation:** Pydantic
*   **Testing & CI/CD:** Pytest, GitHub Actions
*   **Containerization:** Docker

---

### 🚀 Getting Started

Follow these steps to set up and run the project locally.

#### 1. Clone the Repository

```bash
git clone https://github.com/AshwinBalaji007/task-agent.git
cd task-agent
```

#### 2. Create a Virtual Environment

It's highly recommended to use a virtual environment.

```bash
# For Unix/macOS
python3 -m venv .venv
source .venv/bin/activate

# For Windows
python -m venv .venv
.\.venv\Scripts\activate
```

#### 3. Install Dependencies

Install all the required Python libraries.

```bash
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables

You need a Google API key to use the Gemini model.

1.  Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
2.  Open the newly created `.env` file and add your Google API key. You can get one from [Google AI Studio](https://makersuite.google.com/).
    ```ini
    GOOGLE_API_KEY="your_google_api_key_here"
    ```

#### 5. (Optional) Seed the Database

You can run the seed script to populate your database with some sample tasks.

```bash
python -m scripts.seed_database
```

---

### 💻 Usage

You can interact with the agent through the CLI, run the API server, or run the test suite.

#### Run the CLI

This is the main entry point for the application.

```bash
python -m src.main
```
Once running, you can use commands like `list`, `help`, `exit`, or simply type a task you want to add.

#### Run the API Server

The project includes a fully functional FastAPI server.

```bash
uvicorn src.api.endpoints:app --reload
```
You can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

#### Run Tests

Ensure all components are working as expected by running the test suite.

```bash
python -m pytest
```

---

### 📁 Project Structure

The project is organized with a clean, scalable structure:

```
├── .github/      # CI/CD workflows for GitHub Actions
├── configs/      # YAML configuration files (e.g., model settings)
├── docs/         # Documentation and architecture diagrams
├── notebooks/    # Jupyter notebooks for experimentation (prompt tuning, etc.)
├── scripts/      # Utility scripts (e.g., database seeding)
├── src/          # Main source code
│   ├── agent/    # Core agent logic and prompts
│   ├── api/      # FastAPI endpoints
│   ├── core/     # Core components like configuration and logging
│   ├── llm/      # LLM client setup
│   ├── models/   # Pydantic data models
│   └── storage/  # Database interaction logic
└── tests/        # Test suite with pytest
```

---

### 🎥 Video Walkthrough

**Link:** [Your Unlisted YouTube/Vimeo Link Here]
