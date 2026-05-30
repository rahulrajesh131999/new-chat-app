from fastapi import APIRouter
from sqlmodel import Session

from core.depends import Current_User

router = APIRouter(prefix="/conversaion", tags=["conversation"])



@router.post("/create-conversation")
async def create_conversaion(session:Session, user:Current_User):
    return None