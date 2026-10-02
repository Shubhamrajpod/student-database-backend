# Student Database Application System – Backend

A modular backend application for managing student records using FastAPI and SQLAlchemy, with Google Gemini, LangGraph, and ChromaDB integrated for an AI-powered student database chatbot.

## Project Objectives

- Build a modular FastAPI backend.
- Implement Create, Read, Update, and Delete (CRUD) operations for student records.
- Provide automatic Swagger/OpenAPI documentation.
- Integrate Google Gemini API for natural-language chatbot responses.
- Use LangGraph to manage the chatbot workflow.
- Use ChromaDB as the vector database for student information retrieval.
- Keep API keys and sensitive configuration outside the source code.

## Technology Stack

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Pydantic
- Google Gemini API
- LangGraph
- ChromaDB
- python-dotenv

## Project Structure

```text
student-database-backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   │
│   └── chatbot/
│       ├── __init__.py
│       ├── graph.py
│       └── vector_db.py
│
├── .gitignore
├── requirements.txt
└── README.md