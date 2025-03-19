from passlib.context import CryptContext
from app.database.db import db
import jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")