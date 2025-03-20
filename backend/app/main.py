from fastapi import FastAPI
from app.routes.websocket import router as websocket_router
from app.routes.messages import router as messages_router
from app.routes.auth import router as auth_router
from app.routes.chatbots import router as chatbots_router


app = FastAPI(
    title="Chatbot API",
    description="API for chatbot",
    version="0.1",
)

app.include_router(websocket_router)
app.include_router(messages_router)
app.include_router(auth_router)
app.include_router(chatbots_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)