from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import random
from models import Question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

DATA_FILE = "data.json"

async def load_json(file_name: str):
    question_list = []

    if not os.path.exists(file_name):
        raise FileNotFoundError(f"{file_name} not found.")

    with open(file_name, 'r') as file:
        content = file.read().strip()
        if not content:
            raise ValueError(f"{file_name} is empty.")
        data = json.loads(content)

    for item in data:
        question = Question(**item)
        question_list.append(question)
    return question_list

def save_json(file_name: str, questions: list):
    with open(file_name, 'w') as file:
        json.dump([q.dict() if isinstance(q, Question) else q for q in questions], file, indent=4)

@app.get("/questions/", response_model=list[Question])
async def read_questions():
    return await load_json(DATA_FILE)

@app.get("/question/random", response_model=Question)
async def get_random_question():
    questions = await load_json(DATA_FILE)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions available")
    
    selected = random.choice(questions)
    return selected
