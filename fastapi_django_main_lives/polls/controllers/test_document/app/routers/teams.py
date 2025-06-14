from fastapi import APIRouter, Depends
from fastapi.security.utils import get_authorization_scheme
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Team
from app.schemas import TeamSchema
from app.main import async_session

router = APIRouter()

@router.post("/teams/")
async def create_team(name: str, db: AsyncSession = Depends()):
    team = Team(name=name)
    db.add(team)
    await db.commit()
    return {"message": "Team created successfully"}

@router.get("/teams/")
async def read_teams(db: AsyncSession = Depends()):
    teams = await db.execute(Team.__table__.select())
    return [{"name": team.name} for team in teams]