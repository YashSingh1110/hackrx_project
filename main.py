# main.py

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from typing import List
from rag_pipeline import get_answers_from_documents

# Initialize the FastAPI app
app = FastAPI(
    title="HackRx 6.0 RAG API",
    description="An API to answer questions about documents using a RAG pipeline."
)

# --- Define the request and response models ---
# This ensures the incoming data and outgoing data match the hackathon's format.

class QueryRequest(BaseModel):
    documents: str = Field(..., description="URL of the document to process.")
    questions: List[str] = Field(..., description="List of questions to answer.")

class QueryResponse(BaseModel):
    answers: List[str]

# --- API Endpoints ---

@app.get("/")
def read_root():
    """A simple endpoint to check if the API is running."""
    return {"status": "ok", "message": "Welcome to the HackRx RAG API!"}


@app.post("/hackrx/run", response_model=QueryResponse)
async def run_submission(
    request: QueryRequest, 
    authorization: str = Header(None)
):
    """
    This is the main endpoint for the hackathon submission.
    It receives a document URL and questions, and returns answers.
    """
    # Note: The hackathon docs mention a Bearer token. 
    # In a real app, you would validate it here.
    # For now, we'll just print it.
    print(f"Received authorization header: {authorization}")

    # Call our core logic from the other file
    answers = get_answers_from_documents(
        doc_url=request.documents, 
        questions=request.questions
    )
    
    # Return the answers in the specified format
    return QueryResponse(answers=answers)