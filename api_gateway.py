from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_app import rag_app  # Import the initialized RAGApp instance

app = FastAPI()

# Pydantic model for the request body
class Question(BaseModel):
    question: str

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.post("/ask")
async def ask_question(question: Question, pdf: UploadFile = File(...)):
    try:
        # Process the uploaded PDF and create a retriever
        retriever = rag_app.process_pdf(pdf)
        
        # Get the answer to the question based on the PDF content
        answer = rag_app.get_answer(question.question, retriever)
        
        # Return the question and the generated answer
        return {"question": question.question, "answer": answer}
    
    except Exception as e:
        # Handle exceptions and return an appropriate error message
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "API is running successfully"}
