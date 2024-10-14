from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from query_handler import handle_query
from student_kbc import generate_question
from document_loader import load_documents
import random
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chunks = load_documents("data/ncert.pdf")

class Query(BaseModel):
    question: str

class QuizResponse(BaseModel):
    question: str
    options: dict
    correct_answer: str

class TranslateRequest(BaseModel):
    text: str  

@app.post("/query/")
async def query_notes(query: Query):
    response = handle_query(query.question, chunks)
    return {"response": response["response"]}

@app.get("/generate-question/")
def get_question():
    if not chunks:
        raise HTTPException(status_code=404, detail="No documents loaded.")
    
    context = random.choice(chunks).page_content 

    question = generate_question(context)
    
    return {"question": question}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
