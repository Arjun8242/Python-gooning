from datetime import datetime
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict


# User Schemas
class UserCreate(BaseModel):
    username: str
    email: str
    password: str



class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    user_id: int | None = None


# Note Schemas
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
    owner_id: int | None = None

    model_config = ConfigDict(from_attributes=True)



