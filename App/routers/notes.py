from fastapi import APIRouter
from fastapi import HTTPException,Depends
from pracmodel import Note,CreateNote,UpdateNote,Base,NoteResponse
from crud import getnote,addnote,updatenote,deletenote
from DataBase import SessionLocal, engine, get_db


note_router = APIRouter()
Base.metadata.create_all(bind = engine) #creates a table in mysql

@note_router.get("/{note_id}",response_model=NoteResponse,status_code=200) #changed the endpoint to standard api endpoints
def get_note(note_id: int,db:SessionLocal = Depends(get_db)):
    find_note = getnote(note_id,db)
    if find_note is None:
       raise HTTPException(status_code=404, detail="Note not found!")
    return find_note


@note_router.post("/",response_model = NoteResponse,status_code=201)
def add_note(note:CreateNote,db:SessionLocal = Depends(get_db)):
    new_note = Note(note_id = note.note_id,title = note.title,content = note.content)
    new_note = addnote(new_note,db)
    if new_note is not None:
        return new_note
    raise HTTPException(status_code=400, detail="Note not added!")

@note_router.put("/{id}",response_model = NoteResponse,status_code=200)
def update_note(id:int,content:UpdateNote,db:SessionLocal = Depends(get_db)):
    updated = updatenote(Note,content,id,db)
    if updated is not None:
        return updated
    raise HTTPException(status_code=404, detail="Note not found!")


@note_router.delete("/{id}",status_code=204)
def delete_note(id:int,db:SessionLocal = Depends(get_db)):
    deleted = deletenote(Note,id,db)
    if deleted:
        return "Note deleted Successfully!"
    raise HTTPException(status_code=404, detail="Note not found!")

