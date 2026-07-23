# pyrefly: ignore [missing-import]
from pydantic import BaseModel

class NoteCreate(BaseModel):
    title: str
    content: str
    tags: list[str] = []

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    tags: list[str]
