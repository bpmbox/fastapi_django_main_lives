from .models import User, Team
from .database import SessionLocal

def get_users(db: Session):
    return db.query(User).all()

def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, profile=user.profile)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.name = user.name
        db_user.profile = user.profile
        db.commit()
        db.refresh(db_user)
    return db_user

def create_team(db: Session, team: TeamCreate):
    db_team = Team(name=team.name)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def get_teams(db: Session):
    return db.query(Team).all()

def get_team(db: Session, team_id: int):
    return db.query(Team).filter(Team.id == team_id).first()