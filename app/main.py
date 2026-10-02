from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import crud, models, schemas
from app.chatbot.graph import chatbot_graph
from app.chatbot.vector_db import add_student_to_vector_db, delete_student_from_vector_db
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Database Application System - Backend",
    version="1.0.0",
    description=(
        "Modular backend with CRUD operations, Vector DB (ChromaDB), and LangGraph Gemini"
        " chatbot."
    ),
)


@app.get("/", tags=["Health"])
def root():
    return {
        "system": "Student Database Backend API",
        "status": "online",
        "docs": "/docs"
    }


@app.post(
    "/students/",
    response_model=schemas.StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Student Management"],
)
def create_student(
    student: schemas.StudentCreate, db: Session = Depends(get_db)
):
  try:
    db_student = crud.create_student(db=db, student=student)
  except IntegrityError:
    db.rollback()
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Email '{student.email}' is already registered."
    )

  # Auto-sync with ChromaDB vector store
  details = f"Student {db_student.name} (Email: {db_student.email}) is enrolled in {db_student.course} semester {db_student.semester}."
  add_student_to_vector_db(
      student_id=db_student.id,
      name=db_student.name,
      course=db_student.course,
      details=details
  )

  return db_student


@app.get(
    "/students/",
    response_model=list[schemas.StudentResponse],
    tags=["Student Management"],
)
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  return crud.get_students(db, skip=skip, limit=limit)


@app.get(
    "/students/{student_id}",
    response_model=schemas.StudentResponse,
    tags=["Student Management"],
)
def read_student(student_id: int, db: Session = Depends(get_db)):
  db_student = crud.get_student(db, student_id=student_id)
  if db_student is None:
    raise HTTPException(status_code=404, detail="Student not found")
  return db_student


@app.put(
    "/students/{student_id}",
    response_model=schemas.StudentResponse,
    tags=["Student Management"],
)
def update_student(
    student_id: int,
    student: schemas.StudentUpdate,
    db: Session = Depends(get_db),
):
  try:
    db_student = crud.update_student(db=db, student_id=student_id, student=student)
  except IntegrityError:
    db.rollback()
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Updated email is already in use by another student."
    )

  if db_student is None:
    raise HTTPException(status_code=404, detail="Student not found")

  # Auto-sync update to ChromaDB vector store
  details = f"Student {db_student.name} (Email: {db_student.email}) is enrolled in {db_student.course} semester {db_student.semester}."
  add_student_to_vector_db(
      student_id=db_student.id,
      name=db_student.name,
      course=db_student.course,
      details=details
  )

  return db_student


@app.delete("/students/{student_id}", tags=["Student Management"])
def delete_student(student_id: int, db: Session = Depends(get_db)):
  db_student = crud.delete_student(db=db, student_id=student_id)
  if db_student is None:
    raise HTTPException(status_code=404, detail="Student not found")

  # Auto-remove from ChromaDB vector store
  delete_student_from_vector_db(student_id=student_id)

  return {"message": "Student deleted successfully"}


class ChatRequest(BaseModel):
  query: str


@app.post("/chat/", tags=["AI Chatbot"])
def chat_with_database(request: ChatRequest):
  initial_state = {"query": request.query, "context": "", "response": ""}
  output = chatbot_graph.invoke(initial_state)
  return {"query": request.query, "response": output["response"]}