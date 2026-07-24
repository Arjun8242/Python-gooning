from fastapi import FastAPI
from app.routers import notes, auth
from app.database import Base, engine

# create db tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Notes API with JWT Authentication",
    description="FastAPI application with PostgreSQL, SQLAlchemy ORM, and JWT Auth",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(notes.router)


@app.get('/')
def home():
    return {'message': 'Hello World'}