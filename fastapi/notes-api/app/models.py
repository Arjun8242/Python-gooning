from datetime import datetime

# pyrefly: ignore [missing-import]
from app.database import Base

# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, JSON, DateTime


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable = False)#nullable means can't be null
    content = Column(String, nullable = False)
    tags = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)


#base is used to map our python code to the database tables
#only create base one time and rest of the times import that base

