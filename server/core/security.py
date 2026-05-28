from pwdlib import PasswordHash
from datetime import timedelta, datetime, timezone
import jwt

from core.config import settings

password_hash = PasswordHash.recommended()

def hash_password(*,plain_password:str):
    return password_hash.hash(password=plain_password)

def verify_password(*,plain_password:str, hash:str):
    return password_hash.verify(password=plain_password, hash=hash)


def create_token(*,data:str, expires_at:timedelta | None= None):
    if expires_at:
        expire = datetime.now(timezone.utc) + expires_at
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode = ({"exp":expire, "data":str(data)})

    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWL_ALGORITHM)

    return encoded_jwt

def decode_token(*, access_token):
    return jwt.decode(access_token, settings.JWT_SECRET, algorithms=settings.JWL_ALGORITHM)

    