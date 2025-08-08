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
USED_FILE = "used_questions.json"

async def load_json(file_name: str):
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"{file_name} not found.")

    with open(file_name, 'r') as file:
        content = file.read().strip()
        if not content:
            raise ValueError(f"{file_name} is empty.")
        return json.loads(content)

def save_json(file_name: str, data: list):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

@app.get("/questions/", response_model=list[Question])
async def read_questions():
    data = await load_json(DATA_FILE)
    return [Question(**item) for item in data]

@app.get("/question/random", response_model=Question)
async def get_random_question():
    all_questions = await load_json(DATA_FILE)
    used_ids = []

    # Load or initialize used questions
    if os.path.exists(USED_FILE):
        used_ids = await load_json(USED_FILE)

    unused_questions = [q for q in all_questions if q['id'] not in used_ids]

    if not unused_questions:
        # Reset used list and start over
        save_json(USED_FILE, [])
        unused_questions = all_questions

    selected = random.choice(unused_questions)

    # Save selected ID
    used_ids.append(selected['id'])
    save_json(USED_FILE, used_ids)

    return Question(**selected)
