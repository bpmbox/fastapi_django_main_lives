"""
Polls FastAPI Schemas
=====================

Pydantic models for API serialization
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class FastQuestion(BaseModel):
    """質問のFastAPIスキーマ"""
    id: int
    question_text: str
    pub_date: datetime
    
    class Config:
        from_attributes = True  # Pydantic v2対応
        
    @classmethod
    def from_orm(cls, question):
        """DjangoモデルからPydanticモデルに変換"""
        return cls(
            id=question.id,
            question_text=question.question_text,
            pub_date=question.pub_date
        )


class FastQuestions(BaseModel):
    """質問リストのFastAPIスキーマ"""
    questions: List[FastQuestion]
    
    @classmethod
    def from_qs(cls, questions):
        """Django QuerySetからPydanticモデルに変換"""
        return cls(
            questions=[FastQuestion.from_orm(q) for q in questions]
        )


class FastChoice(BaseModel):
    """選択肢のFastAPIスキーマ"""
    id: int
    question_id: int
    choice_text: str
    votes: int
    
    class Config:
        from_attributes = True  # Pydantic v2対応
        
    @classmethod
    def from_orm(cls, choice):
        """DjangoモデルからPydanticモデルに変換"""
        return cls(
            id=choice.id,
            question_id=choice.question.id,
            choice_text=choice.choice_text,
            votes=choice.votes
        )


class FastChoices(BaseModel):
    """選択肢リストのFastAPIスキーマ"""
    choices: List[FastChoice]
    
    @classmethod
    def from_qs(cls, choices):
        """Django QuerySetからPydanticモデルに変換"""
        return cls(
            choices=[FastChoice.from_orm(c) for c in choices]
        )
