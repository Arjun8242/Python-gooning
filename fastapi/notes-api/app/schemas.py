from datetime import datetime
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict

class NoteCreate(BaseModel):
    title: str
    content: str
    tags: list[str] = []

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    tags: list[str] = []
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


