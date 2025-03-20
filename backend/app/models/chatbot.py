from pydantic import BaseModel

class Chatbot(BaseModel):
    id: str
    name: str
    owner: str
    config: dict
