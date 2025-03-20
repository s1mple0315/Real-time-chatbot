import token
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.database.db import db
from app.models.chatbot import Chatbot
import jwt
from app.core.config import settings


router = APIRouter(prefix="/chatbots", tags=["chatbots"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = "initial_key"

def get_current_user(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

prebuilt_chatbots = [
    {"id": "1", "name":"Friendly Bot", "config": {"greeting": "Hi there!"}},
    {"id": "2", "name": "Support Bot", "config": {"greeting": "How can I help?"}},
]


@router.get("/prebuilt")
async def list_prebuilt_chatbots(current_user: str = Depends(get_current_user)):
    return prebuilt_chatbots

@router.get("/embed/{chatbot_id}")
async def get_embed_script(chatbot_id: str, current_user: str = Depends(get_current_user)):
    chatbot = db.get_collection("chatbots").find_one({"id": chatbot_id, "owner": current_user})
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    script = f"""
    <script>
      (function() {{
        const ws = new WebSocket('ws://localhost:8000/ws/{chatbot_id}?token={token}');
        ws.onmessage = (e) => console.log(e.data); // Replace with UI logic
        window.sendChatbotMessage = (msg) => ws.send(msg);
      }})();
    </script>
    """
    return {"script": script}

@router.post("/create")
async def create_chatbot(chatbot_id: str, config: dict, current_user: str = Depends(get_current_user)):
    chatbot = {"id": chatbot_id, "name": prebuilt_chatbots[int(chatbot_id)-1]["name"], "owner": current_user, "config": config}
    db.get_collection("chatbots").insert_one(chatbot)
    return {"message": "Chatbot created", "chatbot": chatbot}

@router.get("/my")
async def list_user_chatbots(current_user: str = Depends(get_current_user)):
    return list(db.get_collection("chatbots").find({"owner": current_user}, {"_id": 0}))
    