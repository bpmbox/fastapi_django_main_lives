from typing import List

from fastapi import APIRouter, Depends

# Laravel構造のサービスを使用
from laravel_app.Services.Polls import retrieve_choices, retrieve_choice
from polls.schemas import FastChoice, FastChoices

router = APIRouter(prefix="/choice", tags=["choices"])


@router.get("/dz", response_model=FastChoices)
async def get_choices() -> FastChoices:
    """全選択肢を取得"""
    choices = await retrieve_choices()
    return FastChoices.from_qs(choices)


@router.get("/{c_id}", response_model=FastChoice)
async def get_choice(choice = Depends(retrieve_choice)) -> FastChoice:
    """特定の選択肢を取得"""
    return FastChoice.from_orm(choice)
