from fastapi import APIRouter
from api.app.schemas import TeamSchema
from api.app.models import Team

router = APIRouter()

@router.post("/teams/")
async def create_team(team: TeamSchema):
    new_team = Team(name=team.name)
    session.add(new_team)
    session.commit()
    return {"message": "Team created successfully"}

@router.get("/teams/")
async def read_teams():
    teams = session.query(Team).all()
    return [{"name": team.name} for team in teams]