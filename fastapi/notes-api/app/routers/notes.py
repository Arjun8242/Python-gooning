from fastapi import Depends
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session


from app.database import get_db
from fastapi import APIRouter, HTTPException
from app.schemas import NoteCreate, NoteResponse
from app.models import Note

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


@router.post("", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(
        title = note.title,
        content = note.content,
        tags = note.tags
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note_data: NoteCreate, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = note_data.title
    note.content = note_data.content
    note.tags = note_data.tags
    db.commit()
    db.refresh(note)
    return note


@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}


@router.get("", response_model=list[NoteResponse])
def get_notes(tags: str | None = None, db: Session = Depends(get_db)):
    notes = db.query(Note).all()
    if tags:
        filtered_notes = []
        for note in notes:
            if note.tags and tags in note.tags:
                filtered_notes.append(note)
        return filtered_notes
    return notes


@router.get("/{note_id}", response_model=NoteResponse)#passing instructions that whatever this function should return, it should match the NoteResponse model
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

