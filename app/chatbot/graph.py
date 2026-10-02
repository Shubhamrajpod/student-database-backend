import os
from typing import TypedDict
from dotenv import load_dotenv
from google import genai
from google.genai import types
from langgraph.graph import END, StateGraph
from app.chatbot.vector_db import query_vector_db

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY", "").strip()
gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()

client = None
if api_key:
  client = genai.Client(api_key=api_key)


# Define state structure for LangGraph using TypedDict
class ChatState(TypedDict):
  query: str
  context: str
  response: str


def retrieve_context_node(state: ChatState):
  query = state["query"]
  search_results = query_vector_db(query)
  documents = search_results.get("documents", [[]])[0]
  context = "\n".join(documents) if documents else "No direct records found in database."
  return {"context": context}


def generate_answer_node(state: ChatState):
  query = state["query"]
  context = state["context"]

  # If GEMINI_API_KEY is configured and client initialized, call Google Gemini
  if client:
    try:
      prompt = (
          f"You are a helpful AI assistant for a student database system.\n"
          f"Use the following student context to answer the user's question safely and accurately.\n\n"
          f"Context:\n{context}\n\n"
          f"Question: {query}\n"
          f"Answer:"
      )

      config = types.GenerateContentConfig(
          automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
      )

      result = client.models.generate_content(
          model=gemini_model,
          contents=prompt,
          config=config,
      )
      return {"response": result.text}
    except Exception as err:
      print(f"[Gemini API Warning] Falling back to context synthesis: {err}")

  # Fallback response generator if API key is not configured or fails
  fallback_text = (
      f"[Student Database Assistant]\n\n"
      f"**Retrieved Context:**\n{context}\n\n"
      f"*(Note: Set GEMINI_API_KEY in .env for full AI natural language responses)*"
  )
  return {"response": fallback_text}


# Build LangGraph Workflow
workflow = StateGraph(ChatState)
workflow.add_node("retrieve", retrieve_context_node)
workflow.add_node("generate", generate_answer_node)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

chatbot_graph = workflow.compile()