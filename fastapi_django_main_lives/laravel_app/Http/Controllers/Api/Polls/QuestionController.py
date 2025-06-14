from typing import List

from fastapi import APIRouter, Depends

# Laravel構造のサービスを使用
from laravel_app.Services.Polls import retrieve_questions, retrieve_question
from polls.schemas import FastQuestion, FastQuestions

router = APIRouter(prefix="/question", tags=["questions"])


@router.get("/cs", response_model=FastQuestions)
async def get_questions() -> FastQuestions:
    """全質問を取得"""
    questions = await retrieve_questions()
    return FastQuestions.from_qs(questions)


@router.get("/{q_id}", response_model=FastQuestion)
async def get_question(
    question = Depends(retrieve_question),
) -> FastQuestion:
    """特定の質問を取得"""
    return FastQuestion.from_orm(question)
