from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.summarize import build_quiz_question, grade_answer

router = APIRouter()

class QuizRequest(BaseModel):
    key_points: List[str]

class GradeRequest(BaseModel):
    question: str
    answer: str
    key_points: List[str]

@router.post("/quiz")
async def quiz(req: QuizRequest):
    return {"question": build_quiz_question(req.key_points)}

@router.post("/quiz/grade")
async def grade(req: GradeRequest):
    return {"feedback": grade_answer(req.question, req.answer, req.key_points)}
