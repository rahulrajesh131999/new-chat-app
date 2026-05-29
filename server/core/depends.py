from sqlmodel import Session
from typing import Annotated
from fastapi import Cookie, HTTPException, status, Depends
import jwt

from core.security import decode_token
from models import User

# getting current user

async def current_user(session:Session, access_token:Annotated[str | None, Cookie(alias="access_token") ]):
    if access_token:
        try:
            payload = await decode_token(access_token=access_token)
            user_id = payload.get("data")

            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="user Id not found, not authenticated"
                )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        
        user = session.get(User, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    
Current_User = Annotated[User, Depends(current_user)]
