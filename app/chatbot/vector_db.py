import chromadb

# Initialize local ChromaDB client for vector search
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="student_records")


def add_student_to_vector_db(
    student_id: int, name: str, course: str, details: str
):
  """Add or update student record in ChromaDB vector database."""
  collection.upsert(
      documents=[details],
      metadatas=[{"name": name, "course": course}],
      ids=[str(student_id)],
  )


def delete_student_from_vector_db(student_id: int):
  """Delete a student vector entry from ChromaDB."""
  try:
    collection.delete(ids=[str(student_id)])
  except Exception as e:
    print(f"[VectorDB Warning] Could not delete ID {student_id} from vector store: {e}")


def query_vector_db(query_text: str, n_results: int = 2):
  """Query ChromaDB for relevant student documents."""
  results = collection.query(query_texts=[query_text], n_results=n_results)
  return results