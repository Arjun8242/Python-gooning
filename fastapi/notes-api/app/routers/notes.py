from fastapi import APIRouter, HTTPException
from app.schemas import NoteCreate, NoteResponse

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

notes = [
    {
        "id":1,
        "title": "Learn FastAPI",
        "content": "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.",
        "tags": ["python", "fastapi"]
    },
    {
        "id":2,
        "title": "Learn Node.js",
        "content": "Node.js is a JavaScript runtime built on the V8 engine that allows you to run JavaScript on the server-side.",
        "tags": ["javascript", "node"]
    }
]

@router.post("")
def create_note(note: NoteCreate):
    note_id = len(notes) + 1
    new_note = {
        'id': note_id,
        'title': note.title,
        'content': note.content,
        'tags': note.tags
    }
    notes.append(new_note)
    return {
        "message": "Note added successfully",
        "note": new_note
    }
#fastapi returns one object


@router.put("/{note_id}")
def update_note(note_id: int, note_data:NoteCreate):
    for note in notes:
        if note['id'] == note_id:
            note['title'] = note_data.title
            note['content'] = note_data.content
            note['tags'] = note_data.tags
            return {
                "message": "Note updated successfully",
                "note": note
            }
    raise HTTPException(status_code=404, detail="Note not found")


@router.delete("/{note_id}")
def delete_note(note_id: int):
    for note in notes:
        if note['id'] == note_id:
            notes.remove(note)
            return {"message": "Note deleted successfully"}
    raise HTTPException(status_code=404, detail="Note not found")


@router.get("", response_model = list[NoteResponse])
def get_notes(tags: str | None = None):
    if tags:
        filtered_notes = []

        for note in notes:
            if tags in note["tags"]:
                filtered_notes.append(note)
        return filtered_notes
    
    return notes

@router.get("/{note_id}", response_model = NoteResponse)#passing instructions that whatever this function should return, it should match the NoteResponse model
def get_note(note_id: int):
    for note in notes:
        if note['id'] == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")
