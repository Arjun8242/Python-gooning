from fastapi import FastAPI
from app.routers import notes
from app.database import Base, engine
from app.models import Note


# create db tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(notes.router)

@app.get('/')
def home():
    return {'message' : 'Hello World'}