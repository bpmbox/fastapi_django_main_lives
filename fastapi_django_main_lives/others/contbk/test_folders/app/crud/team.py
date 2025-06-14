from app.models.team import Team
from app.schema.team import TeamSchema
from sqlalchemy.orm import Session

def create_team(db: Session, team: TeamSchema):
    db_team = Team(name=team.name)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def get_teams(db: Session):
    return db.query(Team).all()