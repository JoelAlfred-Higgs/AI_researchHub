from fastapi import APIRouter
from fastapi import HTTPException,Depends
from pracmodel import Note,CreateNote,UpdateNote,Base
from crud import getnote,addnote,updatenote,deletenote
from DataBase import SessionLocal, engine, get_db

note_router = APIRouter()
Base.metadata.create_all(bind = engine) #creates a table in mysql

@note_router.get("/{note_id}")
def get_note(note_id: int,db:SessionLocal = Depends(get_db)):
    find_note = getnote(note_id,db)
    if find_note is not None:
        return {
            "Note_id": find_note.note_id,
            "Title": find_note.title,
            "content": find_note.content
        }   
    raise HTTPException(status_code=404, detail="Note not found!")
  
@note_router.post("/add_note")
def add_note(note:CreateNote,db:SessionLocal = Depends(get_db)):
    new_note = Note(note_id = note.note_id,title = note.title,content = note.content)
    addnote(new_note,db)
    return "Note added Successfully!"

@note_router.put("/update_note")
def update_note(id:int,content:UpdateNote,db:SessionLocal = Depends(get_db)):
    updated = updatenote(Note,content,id,db)
    if updated is not None:
        return {
            "note_id" : updated.note_id,
            "title":updated.title,
            "content":updated.content
                      } 
    return "Note does not exist!"
@note_router.delete("/delete_note")
def delete_note(id:int,db:SessionLocal = Depends(get_db)):
    deleted = deletenote(Note,id,db)
    if deleted:
        return "Note deleted Successfully!"
    return "Note does not exist!"

