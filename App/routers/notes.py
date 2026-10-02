from fastapi import APIRouter
from fastapi import HTTPException,Depends
from schemas import CreateNote,UpdateNote,NoteResponse
from crud import getnote,addnote,updatenote,deletenote,getallnotes,getallnotes_bycategory
from DataBase import engine, get_db
from sqlalchemy.orm import Session
from models import Note,Base

note_router = APIRouter()
Base.metadata.create_all(bind = engine) #creates a table in mysql

@note_router.get("/{note_id}",response_model=NoteResponse,status_code=200) #changed the endpoint to standard api endpoints
def get_note(note_id: int,db:Session = Depends(get_db)):
    find_note = getnote(note_id,db)
    if find_note is None:
       raise HTTPException(status_code=404, detail="Note not found!")
    return find_note

@note_router.get("/user/{owner_id}", response_model=list[NoteResponse], status_code=200)
def get_all_notes(owner_id: int,db: Session = Depends(get_db)):
    notes = getallnotes(db,owner_id) 
    if notes is None:
        raise HTTPException(status_code=404, detail="No notes found for user!")
    return notes    

@note_router.get("/user/{owner_id}/{categ_id}",response_model = list[NoteResponse],status_code = 200)
def get_notes_bycategory(owner_id:int,categ_id:int,db:Session = Depends(get_db)):
    notes_by_category = getallnotes_bycategory(db,owner_id,categ_id)
    if notes_by_category is None:
        raise HTTPException(status_code=404, detail="No notes found for user!")
    return notes_by_category

@note_router.post("/",response_model = NoteResponse,status_code=201)
def add_note(note:CreateNote,db:Session = Depends(get_db)):
    new_note = Note(owner_id = note.owner_id ,title = note.title,content = note.content,category_id = note.category_id)
    new_note = addnote(new_note,db)
    if new_note is not None:
        return new_note
    raise HTTPException(status_code=409, detail="Note already exists!")

@note_router.put("/{id}",response_model = NoteResponse,status_code=200)
def update_note(id:int,content:UpdateNote,db:Session = Depends(get_db)):
    updated = updatenote(content,id,db)
    if updated is not None:
        return updated
    raise HTTPException(status_code=404, detail="Note not found!")


@note_router.delete("/{owner_id}/{note_id}",status_code=204)
def delete_note(owner_id:int,note_id:int,db:Session = Depends(get_db)):
    deleted = deletenote(note_id,owner_id,db)
    if deleted == 1:
        return  
    raise HTTPException(status_code=404, detail="Note not found!")

