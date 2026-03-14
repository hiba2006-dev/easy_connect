import json
import random

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

import app.auth as auth
import app.models as models
from app.activity import record_activity
from app.database import get_db

MAX_QUIZ_QUESTIONS = 20


class QuizCompletionPayload(BaseModel):
    score: int
    total: int
    percent: int


router = APIRouter(prefix="/api/quiz", tags=["quiz"])


@router.post("/complete")
async def complete_quiz(
    payload: QuizCompletionPayload,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    record_activity(
        db,
        current_user.id,
        "quiz_completion",
        f"Quiz completed {payload.score}/{payload.total} ({payload.percent}%)",
        {"score": payload.score, "total": payload.total, "percent": payload.percent},
    )
    db.commit()
    return {"ok": True}


@router.get("/questions")
async def list_quiz_questions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    questions = (
        db.query(models.QuizQuestion)
        .order_by(models.QuizQuestion.created_at.desc())
        .all()
    )
    payload = []
    for question in questions:
        payload.append(
            {
                "id": question.id,
                "prompt": question.prompt,
                "prompt_media": question.prompt_media,
                "prompt_type": question.prompt_type,
                "answer_index": question.answer_index,
                "category": question.category,
                "options": json.loads(question.options or "[]"),
            }
        )

    unique_questions = list({item["id"]: item for item in payload}.values())
    random.shuffle(unique_questions)
    limited_questions = unique_questions[: min(len(unique_questions), MAX_QUIZ_QUESTIONS)]
    return {"questions": limited_questions}
