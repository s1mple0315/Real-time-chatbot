from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.services.auth import create_user, authenticate_user, create_access_token
from app.database.db import db

router = APIRouter(prefix="/auth", tags=["auth"])

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):  
    username: str
    password: str

@router.post("/register")
async def register(user: UserCreate):
    if db.get_collection("users").find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    create_user(user.username, user.password)
    return {"message": "User created"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    auth_user = authenticate_user(form_data.username, form_data.password)  
    if not auth_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": auth_user["username"]})
    return {"access_token": token, "token_type": "bearer"}