from pydantic import BaseModel

class Question(BaseModel):
    id: int
    question: str
    answer: str
class QuestionBank(BaseModel):
    questions: list[Question]
        
    