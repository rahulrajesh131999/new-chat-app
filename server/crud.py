from sqlmodel import Session, select
from models import User, UserSecure, UserId, Conversation, Conversation_Member
from core.security import hash_password
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from core.security import verify_password
from core.config import settings

# --------------------------User---------------------------------------------------------------

async def create_user(*,session:Session, user:UserSecure):
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

async def authenticate(session:Session, email:str, password:str):

    user = session.exec(select(User).where(User.email == email)).first()

    if not user:
        await verify_password(plain_password=password, hash=settings.DUMMY_HASH)
        return False
    if not verify_password(plain_password=password, hash=user.hashed_password):
        return False
    
    return user



# conversation controllers

async def create_private_conversation(session:Session, user:User, recieverId:UserId):

    if not recieverId:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST, detail="reciever id not provided"
        )
    
    reciever = await session.exec(select(User).where(User.id == recieverId)).first()

    if not reciever:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="reviever not found"
        )
    
    # check if a conversation already exists 

    conversation_exists = await session.exec(select(Conversation))
    
    new_private_conversation = await session
    

