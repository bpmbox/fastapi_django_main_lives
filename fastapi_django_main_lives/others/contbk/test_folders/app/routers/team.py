from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.encoders import jsonable_encoder
from app.crud.team import create_team, get_teams
from app.schema.team import TeamSchema
from app.main import get_db

router = APIRouter()

@router.post("/teams/")
async def create_team_endpoint(team: TeamSchema, db: Session = Depends(get_db)):
    return create_team(db, team)

@router.get("/teams/")
async def get_teams_endpoint(db: Session = Depends(get_db)):
    return get_teams(db)