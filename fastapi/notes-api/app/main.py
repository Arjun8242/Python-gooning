from fastapi import FastAPI

app = FastAPI()

notes = [
    {
        "id":1,
        "title": "Learn FastAPI",
        "contents": "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.",
        "tags": ["python", "fastapi"]
    },
    {
        "id":2,
        "title": "Learn Node.js",
        "contents": "Node.js is a JavaScript runtime built on the V8 engine that allows you to run JavaScript on the server-side.",
        "tags": ["javascript", "node"]
    }
]

@app.get("/notes")
def get_notes():
    return notes

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    return notes[note_id - 1]

@app.get('/')
def home():
    return {'message' : 'Hello World'}