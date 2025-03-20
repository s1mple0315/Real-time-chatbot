from passlib.context import CryptContext
from app.database.db import db
import jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "initial_key"
ALGORITHM = "HS256"

users_collection = db.get_collection("users")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

def create_user(username: str, password:str):
    hashed_password = hash_password(password)
    user = {"username": username, "password": hashed_password}
    users_collection.insert_one(user)
    return user

def authenticate_user(username: str, password: str):
    user = users_collection.find_one({"username": username})
    if user and verify_password(password, user["password"]):
        return user
    return None

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
