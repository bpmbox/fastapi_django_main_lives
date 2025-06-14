from typing import Type, TypeVar

from django.db import models
from fastapi import HTTPException, Path

# Laravel構造の軽量モデルラッパーを使用
from laravel_app.Models.Polls.models_wrapper import get_question_model, get_choice_model

ModelT = TypeVar("ModelT", bound=models.Model)


async def retrieve_object(model_class: Type[ModelT], id: int) -> ModelT:
    instance = await model_class.objects.filter(pk=id).afirst()
    if not instance:
        raise HTTPException(status_code=404, detail="Object not found.")
    return instance


async def retrieve_question(q_id: int = Path(..., description="get question from db")):
    Question = get_question_model()
    if Question is None:
        raise HTTPException(status_code=500, detail="Question model not available")
    return await retrieve_object(Question, q_id)


async def retrieve_choice(c_id: int = Path(..., description="get choice from db")):
    Choice = get_choice_model()
    if Choice is None:
        raise HTTPException(status_code=500, detail="Choice model not available")
    return await retrieve_object(Choice, c_id)


async def retrieve_questions():
    Question = get_question_model()
    if Question is None:
        return []
    return [q async for q in Question.objects.all()]


async def retrieve_choices():
    Choice = get_choice_model()
    if Choice is None:
        return []
    return [c async for c in Choice.objects.all()]
