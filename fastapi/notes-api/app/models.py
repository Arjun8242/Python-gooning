from datetime import datetime

# pyrefly: ignore [missing-import]
from app.database import Base

# pyrefly: ignore [missing-import]
# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    notes = relationship("Note", back_populates="owner")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable = False)#nullable means can't be null
    content = Column(String, nullable = False)
    tags = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner = relationship("User", back_populates="notes")


#base is used to map our python code to the database tables
#only create base one time and rest of the times import that base


