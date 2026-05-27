from sqlmodel import Session
from models import User, UserSecure
from core.security import hash_password
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

# --------------------------User---------------------------------------------------------------

async def create_user(session:Session, user:UserSecure):
    db_object = User.model_validate(
        user, update={"hashed_password", hash_password(plain_password=user.password)}
    )

    try:
        session.add(db_object)
        session.commit()
        session.refresh(db_object)
    except SQLAlchemyError as e:
        session.rollback()
        HTTPException(status_code=500,detail="failed to create user")
    
    return db_object

async def delete_user(session:Session, userId:str):
    return None