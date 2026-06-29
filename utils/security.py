from passlib.context import CryptContext  # pip install bcrypt==4.0.1

from jose import jwt
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from models.user import User

from app.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY=settings.SECRET_KEY            # there contraints after pwd_context
ALGORITHM=settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES=settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # below the constraints

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode=data.copy()
    expire=datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def verify_access_token(token: str):
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

def get_current_user(
        token: str=Depends(oauth2_scheme), db: Session=Depends(get_db)
):
    payload=verify_access_token(token)
    email=payload.get("sub")
    user=db.query(User).filter(User.email==email).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="invalid token"
        )
    return user
