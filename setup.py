from setuptools import setup, find_packages

setup(
    name="task_agent",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # List core dependencies from requirements.txt here
        "langchain",
        "langchain-google-genai",
        "chromadb",
        "pydantic",
        "pydantic-settings",
        "pyyaml",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "task-agent=main:main_cli",
        ],
    },
)