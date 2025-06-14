from fastapi import APIRouter
from app.schemas import TeamSchema
from app.models import Team
from sqlalchemy.orm import sessionmaker

router = APIRouter()

@router.post("/teams/")
async def create_team(name: str):
    team = Team(name=name)
    session.add(team)
    session.commit()
    return {"message": "Team created successfully"}

@router.get("/teams/")
async def read_teams():
    teams = session.query(Team).all()
    return [{"id": team.id, "name": team.name} for team in teams]