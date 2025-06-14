from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..models import Team
from ..schemas import TeamSchema

router = APIRouter()

@router.post("/teams/")
async def create_team(team: TeamSchema, session: Session = Depends()):
    existing_team = session.query(Team).filter_by(name=team.name).first()
            if existing_team:
                raise HTTPException(status_code=400, detail="Team name already exists")
            new_team = Team(name=team.name)
            session.add(new_team)
            session.commit()
            return {"message": "Team created successfully"}