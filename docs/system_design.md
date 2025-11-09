graph TD
    subgraph "User Interface"
        A[CLI / FastAPI Server]
    end

    subgraph "Agent Core (src/agent)"
        B[TaskManagerAgent]
        C[Prompt Template]
        D{Parsing & Validation}
    end

    subgraph "External Services"
        E["(External) Google Gemini LLM"]
    end

    subgraph "Data & Storage (src/storage)"
        F[ChromaDB Vector Store]
    end

    subgraph "Data Models (src/models)"
        G[LLMTaskSchema]
        H[Full 'Task' Model]
    end

    A -- "1. User Query (raw text)" --> B
    B -- "2. Format Prompt" --> C
    C -- "3. Complete Prompt" --> B
    B -- "4. Send to LLM" --> E
    E -- "5. Raw Output (string w/ Markdown)" --> B
    B -- "6. Sanitize & Parse" --> D
    D -- "7. Parsed Data" --> G
    B -- "8. Check for Duplicate (by title)" --> F
    F -- "9. Exists? (True/False)" --> B
    B -- "10. Upgrade to Full Model" --> H
    B -- "11. Save Task" --> F
    B -- "12. Return Success" --> A
