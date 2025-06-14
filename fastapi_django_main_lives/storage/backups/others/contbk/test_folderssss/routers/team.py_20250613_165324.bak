from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from database import engine, SessionLocal
from models.team import Team
from schemas.team import TeamCreate, TeamRead

router = APIRouter()

@router.get("/api/teams")
async def read_teams(db: SessionLocal = Depends()):
    teams = db.query(Team).all()
    return JSONResponse(status_code=200, content=[TeamRead.from_orm(team) for team in teams])

@router.post("/api/teams")
async def create_team(team: TeamCreate, db: SessionLocal = Depends()):
    new_team = Team(name=team.name)
    db.add(new_team)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Team created successfully"})