from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import TeamCreate, Team
from app.models import Team as TeamModel

router = APIRouter()

@router.post("/teams/")
def create_team(team: TeamCreate, db: Session = Depends()):
    new_team = TeamModel(name=team.name)
    db.add(new_team)
    db.commit()
    return {"message": "Team created successfully"}

@router.get("/teams/")
def read_teams(db: Session = Depends()):
    teams = db.query(TeamModel).all()
    return [{"id": team.id, "name": team.name, "created_at": team.created_at} for team in teams]