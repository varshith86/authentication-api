from pydantic import BaseModel, EmailStr  #pip install email-validator

class UserRegister(BaseModel):
    username: str
    email:EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    