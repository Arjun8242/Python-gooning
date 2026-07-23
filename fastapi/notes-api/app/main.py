from fastapi import FastAPI
from app.routers import notes

app = FastAPI()

app.include_router(notes.router)

@app.get('/')
def home():
    return {'message' : 'Hello World'}