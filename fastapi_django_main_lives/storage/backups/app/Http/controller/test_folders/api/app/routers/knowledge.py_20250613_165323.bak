from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..models import Knowledge

router = APIRouter()

@router.post("/knowledge/")
async def create_knowledge(knowledge: Knowledge, session: Session = Depends()):
    existing_knowledge = session.query(Knowledge).filter_by(term=knowledge.term).first()
    if existing_knowledge:
        raise HTTPException(status_code=400, detail="Knowledge term already exists")
    new_knowledge = Knowledge(term=knowledge.term, description=knowledge.description)
    session.add(new_knowledge)
    session.commit()
    return {"message": "Knowledge created successfully"}