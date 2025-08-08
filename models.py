from pydantic import BaseModel

class Question(BaseModel):
    question: str
    answer: str
class QuestionBank(BaseModel):
    questions: list[Question]
        
    