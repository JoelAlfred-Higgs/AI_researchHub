from fastapi import APIRouter
from fastapi import HTTPException,Depends
from schemas import CreateNote,UpdateNote,NoteResponse
from crud import getnote,addnote,updatenote,deletenote,getallnotes,getallnotes_bycategory
from DataBase import engine, get_db
from sqlalchemy.orm import Session
from models import Note,Base,User
from dependencies import get_current_user

note_router = APIRouter()
Base.metadata.create_all(bind = engine) #creates a table in mysql

@note_router.get("/mine", response_model=list[NoteResponse], status_code=200)
def get_all_notes(current_user : User = Depends(get_current_user) ,db: Session = Depends(get_db)):
    return getallnotes(db,current_user.user_id) 


@note_router.get("/{note_id}",response_model=NoteResponse,status_code=200) #changed the endpoint to standard api endpoints
def get_note(note_id: int,db:Session = Depends(get_db)):
    find_note = getnote(note_id,db)
    if find_note is None:
       raise HTTPException(status_code=404, detail="Note not found!")
    return find_note

 

@note_router.get("/user/{owner_id}/{categ_id}",response_model = list[NoteResponse],status_code = 200)
def get_notes_bycategory(owner_id:int,categ_id:int,db:Session = Depends(get_db)):
    notes_by_category = getallnotes_bycategory(db,owner_id,categ_id)
    if notes_by_category is None:
        raise HTTPException(status_code=404, detail="No notes found for user!")
    return notes_by_category

@note_router.post("/",response_model = NoteResponse,status_code=201)
def add_note(note:CreateNote,current_user : User = Depends(get_current_user),db:Session = Depends(get_db)):
    new_note = Note(owner_id = current_user.user_id ,title = note.title,content = note.content,category_id = note.category_id)
    res = addnote(new_note,db)
    if res is not None:
        return res
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

