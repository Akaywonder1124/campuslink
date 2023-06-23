from passlib.context import CryptContext
from typing import Any
from jose import jwt
from app.core.config import settings
from datetime import timedelta, datetime


ALGORITHM = "HS256"

def create_access_token(subject : str | Any,  scopes : list, expire_delta : timedelta = None):
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    token_data = {
        "exp" : expire,
        "sub" : str(subject),
        "scopes" : scopes 
    }

    token_encoded = jwt.encode(token_data, settings.SECRET_KEY, ALGORITHM)
    return token_encoded

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
