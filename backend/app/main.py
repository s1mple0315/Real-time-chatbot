from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.database import save_message, get_all_messages

app = FastAPI(
    title="Chatbot WebSocket API",
    description="A simple FastAPI backend with WebSocket and MongoDB for real-time chat.",
    version="1.0.0"
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            save_message(data, "user")  
            response = "Hi! You said: " + data
            await manager.send_personal_message(response, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("A client disconnected")

@app.get("/messages", summary="Get all stored messages", response_description="List of messages")
async def read_messages():
    return get_all_messages()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)