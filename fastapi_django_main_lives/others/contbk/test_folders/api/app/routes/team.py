from fastapi import APIRouter
from . import crud
from . import schema

router = APIRouter()

@router.post("/teams/")
def create_team(team: schema.TeamCreate):
    return crud.create_team(team=team)

@router.get("/teams/")
def read_teams(skip: int = 0, limit: int = 100):
    return crud.get_teams(skip=skip, limit=limit)

@router.get("/teams/{team_id}")
def read_team(team_id: int):
    return crud.get_team(team_id=team_id)