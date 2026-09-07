from fastapi import APIRouter
from fastapi import HTTPException,Depends
from pracmodel import Note,CreateNote,UpdateNote,Base,NoteResponse
from crud import getnote,addnote,updatenote,deletenote
from DataBase import SessionLocal, engine, get_db


note_router = APIRouter()
Base.metadata.create_all(bind = engine) #creates a table in mysql

@note_router.get("/{note_id}") #changed the endpoint to standard api endpoints
def get_note(note_id: int,db:SessionLocal = Depends(get_db)):
    find_note = getnote(note_id,db)
    if find_note is not None:
        response_model = NoteResponse(note_id = find_note.note_id , title = find_note.title, content = find_note.content)
        return response_model 
    raise HTTPException(status_code=404, detail="Note not found!")
  
@note_router.post("/{id}")
def add_note(note:CreateNote,db:SessionLocal = Depends(get_db)):
    new_note = Note(note_id = note.note_id,title = note.title,content = note.content)
    new_note = addnote(new_note,db)
    if new_note is not None:
        response_model = NoteResponse(note_id = new_note.note_id , title = new_note.title, content = new_note.content)
        return response_model 
    return "Note added Successfully!"

@note_router.put("/{id}")
def update_note(id:int,content:UpdateNote,db:SessionLocal = Depends(get_db)):
    updated = updatenote(Note,content,id,db)
    if updated is not None:
        response_model = NoteResponse(note_id = updated.note_id , title = updated.title, content = updated.content)
        return response_model  
    return "Note does not exist!"
@note_router.delete("/{id}")
def delete_note(id:int,db:SessionLocal = Depends(get_db)):
    deleted = deletenote(Note,id,db)
    if deleted:
        return "Note deleted Successfully!"
    return "Note does not exist!"

