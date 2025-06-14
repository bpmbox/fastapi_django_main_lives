from fastapi import APIRouter
from app.schemas import TeamSchema
from app.models import Team
from sqlalchemy.orm import sessionmaker

router = APIRouter()

@router.post("/teams/")
async def create_team(name: str):
    team = Team(name=name)
    session = sessionmaker(bind=engine)()
    session.add(team)
    session.commit()
    return {"message": "Team created successfully"}

@router.get("/teams/")
async def read_teams():
    session = sessionmaker(bind=engine)()
    teams = session.query(Team).all()
    return [TeamSchema.from_orm(team) for team in teams]