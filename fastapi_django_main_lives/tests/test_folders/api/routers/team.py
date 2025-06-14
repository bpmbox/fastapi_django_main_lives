from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from models import Team
from schemas import TeamSchema

router = APIRouter()

@router.post("/teams")
async def create_team(team: TeamSchema, db: Session = Depends()):
    new_team = Team(name=team.name)
    db.add(new_team)
    db.commit()
    return {"message": "Team created successfully"}