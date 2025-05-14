
from pydantic import BaseModel, Field


class SendMessage(BaseModel):
    chat_id: str
    text: str = None
    context: dict = {}
    tool_answers: dict = {}


class ChatStatus(BaseModel):
    chat_id: str
