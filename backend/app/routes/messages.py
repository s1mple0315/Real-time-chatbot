from fastapi import APIRouter
from app.database.db import get_all_messages

router = APIRouter(tags=["REST routes"])

@router.get("/messages")
async def get_messages():
    return get_all_messages()