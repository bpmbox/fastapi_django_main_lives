from fastapi import APIRouter
from app.schemas import UserSchema
from app.models import User
from sqlalchemy.orm import sessionmaker

router = APIRouter()

@router.get("/profiles/{user_id}")
async def read_profile(user_id: int):
    session = sessionmaker(bind=engine)()
    user = session.query(User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserSchema.from_orm(user)