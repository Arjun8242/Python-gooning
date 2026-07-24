# pyrefly: ignore [missing-import]
from sqlalchemy import create_engine
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:Arjun8242@localhost:5433/notes-api-fastapi"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#we use yield instead of return 
#return means it will return the value and exit the function
#yield means it will return the value and pause the function
#finally means it will execute the code after the function is exited

#yield is generator function
#generator functions can only be used in dependency injection