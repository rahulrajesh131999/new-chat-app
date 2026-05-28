from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from datetime import timedelta

from models import UserSecure, User, UserRead, UserLogin
from crud import create_user
from core.config import settings
from core.security import create_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def create_new_user(user:UserSecure, session:Session):
    existing_user = session.exec(select(User).where(user.email == User.email)).first()

    if(existing_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered")
    
    created_user = await create_user(user=user, session=session)

    accesss_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_DAYS)

    access_token = await create_token(data=str(create_user.id), expires_at=accesss_token_expires)

    db_object = UserRead.model_validate(created_user)

    response = JSONResponse(
        content={"user": db_object.model_dump(mode="json")}
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age= 28 * 24 * 60 * 60 
    )

    return response


# login

@router.post("/login")
async def login(session:Session, data:UserLogin):
    return None