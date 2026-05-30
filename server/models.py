from sqlmodel import SQLModel, Field
from sqlalchemy import DateTime
from pydantic import EmailStr, BaseModel
from datetime import datetime, timezone
import uuid


def get_date_utc() -> datetime:
    return datetime.now(timezone.utc)


# User model

class UserBase(SQLModel):
    full_name : str = Field(min_length=3)
    email : EmailStr = Field(unique=True, nullable=False)

class UserSecure(UserBase):
    password : str = Field(min_length=8, max_length=24)

class User(UserBase, table=True):
    id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password : str
    created_at : datetime | None = Field(
        default_factory=get_date_utc(), 
        sa_type=DateTime(timezone=True)
        )

class UserRead(UserBase):
    id: uuid.UUID
    created_at : datetime

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class UserId(BaseModel):
    id : uuid.UUID
    
# conversation

class Conversation(SQLModel, table= True):
    id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    is_group : bool
    name : str | None = Field(default=None)
    created_by : uuid.UUID = Field(foreign_key="user.id", nullable= False, ondelete="CASCADE")
    created_at : datetime | None = Field(
        default_factory=get_date_utc(), 
        sa_type=DateTime(timezone=True)
        )
    
# conversation members

class Conversation_Member(SQLModel, table=True):
    id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id : uuid.UUID = Field(foreign_key="conversation.id", nullable=False, ondelete="CASCADE")
    user_id : uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    created_at : datetime | None = Field(
        default_factory=get_date_utc(), 
        sa_type=DateTime(timezone=True)
        )
    
# messages

class Messages(SQLModel, table=True):
    id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    sender_id : uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    content : str | None = Field(default=None)
    created_at : datetime | None = Field(
        default_factory=get_date_utc(), 
        sa_type=DateTime(timezone=True)
        )