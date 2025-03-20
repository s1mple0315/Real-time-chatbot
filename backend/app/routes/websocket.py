from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.utils.websocket_manager import manager
from app.database.db import save_message, db
from app.services.chatbot import get_chatbot_response
from app.routes.chatbots import get_current_user
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(tags=["websocket"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.websocket("/ws/{chatbot_id}")
async def websocket_endpoint(websocket: WebSocket, chatbot_id: str, token: str = Depends(oauth2_scheme)):
    await manager.connect(websocket)
    user = get_current_user(token)
    chatbot = db.get_collection("chatbots").find_one({"id": chatbot_id, "owner": user})
    if not chatbot:
        await websocket.close(code=1008, reason="Invalid chatbot ID or ownership")
        return
    try:
        while True:
            data = await websocket.receive_text()
            save_message(data, user)
            response = get_chatbot_response(data)  # Could use chatbot["config"] later
            await manager.send_personal_message(response, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{user} disconnected")