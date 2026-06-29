from fastapi import FastAPI
from app.config import settings
from app.database import engine
from app.database import Base
from models.user import User
from routers.auth import router as auth_router

Base.metadata.create_all(bind=engine) # this line must be above creating fastAPI

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)

app.include_router(auth_router)  # this line must be above creating fastAPI

@app.get("/")
def home():
    return {
        "message": "Authentication API running"
    }

@app.get("/health")
def health():
    with engine.connect():
        return {
            "database": "connected"
        }