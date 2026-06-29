from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from schemas.user import UserRegister
from models.user import User

from utils.security import hash_password

from fastapi import HTTPException
from schemas.user import UserLogin
from utils.security import verify_password

from utils.security import create_access_token

from utils.security import get_current_user

from fastapi.security import OAuth2PasswordRequestForm  # pip install python-multipart

router = APIRouter()

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="email already registered"
        )
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    return {
        "message": "User registered successfully"
    }

@router.post("/login")
# def login(user: UserLogin, db: Session = Depends(get_db)):
def login(form_data: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="invalid username or password"
        )

    access_token = create_access_token({
        "sub": db_user.email
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/profile")
def profile(current_user: User=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }