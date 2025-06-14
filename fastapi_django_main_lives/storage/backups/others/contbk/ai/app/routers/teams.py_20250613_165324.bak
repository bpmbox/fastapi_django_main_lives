from fastapi import APIRouter
from app.schemas import TeamSchema
from app.models import Team

router = APIRouter()

@router.post("/teams")
async def create_team(team: TeamSchema):
    new_team = Team(name=team.name)
    db.session.add(new_team)
    db.session.commit()
    return {"message": "Team created successfully"}

@router.get("/teams")
async def get_teams():
    teams = Team.query.all()
    return [{"id": team.id, "name": team.name} for team in teams]