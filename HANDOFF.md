# 🚀 Project Developer Handoff Guide

## 📌 Project Overview

This project is a **FastAPI Backend Application for a Student Database Management System**, integrated with:
1. **SQLAlchemy & SQLite**: Relational database for Student records (`name`, `email`, `course`, `semester`).
2. **ChromaDB**: Local vector database for semantic search and RAG retrieval.
3. **LangGraph & Google Gemini**: State graph workflow agent for intelligent database query handling.

---

## 📂 File Structure & Responsibilities

```text
student-database-backend/
│
├── app/
│   ├── __init__.py          # Python package initialization
│   ├── main.py              # FastAPI app routes, auto-sync logic & error handling
│   ├── database.py          # SQLAlchemy SQLite connection setup & get_db dependency
│   ├── models.py            # SQLAlchemy ORM Student table schema
│   ├── schemas.py           # Pydantic V2 request & response validation schemas
│   ├── crud.py              # Database query logic (create, read, update, delete)
│   └── chatbot/
│       ├── __init__.py      # Chatbot package initialization
│       ├── graph.py         # LangGraph workflow (retrieve_context -> generate_answer)
│       └── vector_db.py     # ChromaDB vector store integration (upsert, query, delete)
│
├── .env                     # Environment configuration (Add your GEMINI_API_KEY here)
├── .gitignore               # Excludes virtual envs, database files & vector storage
├── requirements.txt         # Dependencies (FastAPI, SQLAlchemy, ChromaDB, LangGraph, etc.)
└── README.md                # Project documentation
```

---

## ⚡ Quick Setup Instructions for Colleague

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Add Gemini API Key
Open [`.env`](file:///c:/Users/Asus/Desktop/TIMEPASS%20PROJECTS/student-database-backend/.env) and add your Google Gemini API Key:
```env
GEMINI_API_KEY="AIzaSyYourActualGeminiApiKeyHere"
```

### Step 3: Run the Server
```bash
uvicorn app.main:app --reload --port 8000
```

- **Interactive API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🛠️ Where to Make Future Changes

| Goal | Target File | Notes |
| :--- | :--- | :--- |
| **Add / Modify Database Fields** | [`app/models.py`](file:///c:/Users/Asus/Desktop/TIMEPASS%20PROJECTS/student-database-backend/app/models.py) & [`app/schemas.py`](file:///c:/Users/Asus/Desktop/TIMEPASS%20PROJECTS/student-database-backend/app/schemas.py) | Update SQLAlchemy model fields and corresponding Pydantic schemas. |
| **Change DB Operations / Filters** | [`app/crud.py`](file:///c:/Users/Asus/Desktop/TIMEPASS%20PROJECTS/student-database-backend/app/crud.py) | Add custom queries or search filters. |
| **Customize Vector Search** | [`app/chatbot/vector_db.py`](file:///c:/Users/Asus/Desktop/TIMEPASS%20PROJECTS/student-database-backend/app/chatbot/vector_db.py) | Adjust ChromaDB collection name, persistence path, or similarity search parameters. |
| **Modify AI Chatbot Prompt & Logic** | [`app/chatbot/graph.py`](file:///c:/Users/TIGERPC/Desktop/student-database-backend/app/chatbot/graph.py) | Update Gemini system prompt, model choice (`gemini-2.5-flash`), or graph workflow nodes. |
| **Add New API Endpoints** | [`app/main.py`](file:///c:/Users/Asus/Desktop/TIMEPASS%20PROJECTS/student-database-backend/app/main.py) | Register new routes with FastAPI decorators. |

---

## 🧪 How to Run Tests
To verify all CRUD operations, vector DB sync, and chatbot endpoints:
```bash
python -m py_compile app/main.py
```
