from fastapi import APIRouter
from app.schemas import TeamSchema
from app.models import Team
from sqlalchemy.orm import sessionmaker

router = APIRouter()

@router.post("/teams")
async def create_team(team: TeamSchema):
    new_team = Team(name=team.name)
    session.add(new_team)
    session.commit()
    return {"message": "Team created successfully"}

@router.get("/teams")
async def get_teams():
    teams = session.query(Team).all()
    return [{"name": team.name} for team in teams]