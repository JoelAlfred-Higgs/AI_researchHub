from fastapi import APIRouter
from fastapi import HTTPException,Depends
from ..schemas import CreateNote, UpdateNote, NoteResponse
from ..crud import getnote, addnote, updatenote, deletenote, getallnotes, getallnotes_bycategory
from ..DataBase import get_db
from sqlalchemy.orm import Session
from ..models import Note, User, Category
from ..dependencies import get_current_user

note_router = APIRouter()


@note_router.get("/mine", response_model=list[NoteResponse], status_code=200)
def get_all_notes(current_user : User = Depends(get_current_user) ,db: Session = Depends(get_db)):
    return getallnotes(db,current_user.user_id) 


@note_router.get("/mine/category/{categ_id}",response_model = list[NoteResponse],status_code = 200)
def get_notes_bycategory(categ_id:int,current:User = Depends(get_current_user),db:Session = Depends(get_db)):
    notes_by_category = getallnotes_bycategory(db,current.user_id,categ_id)
    return notes_by_category


@note_router.get("/{note_id}",response_model=NoteResponse,status_code=200) #changed the endpoint to standard api endpoints
def get_note(note_id: int,current:User = Depends(get_current_user),db:Session = Depends(get_db)):
    find_note = getnote(note_id, db, current.user_id)
    if find_note is None:
       raise HTTPException(status_code=404, detail="Note not found!")
    return find_note


@note_router.post("/", response_model=NoteResponse, status_code=201)
def add_note(
    note: CreateNote,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.categ_id == note.category_id,
        Category.owner_id == current_user.user_id
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    new_note = Note(
        owner_id=current_user.user_id,
        title=note.title,
        content=note.content,
        category_id=note.category_id
    )

    result = addnote(new_note, db)

    if result is None:
        raise HTTPException(
            status_code=409,
            detail="Note could not be created"
        )

    return result


@note_router.put("/{note_id}",response_model = NoteResponse,status_code=200)
def update_note(note_id:int,content:UpdateNote,current:User = Depends(get_current_user),db:Session = Depends(get_db)):
    updated = updatenote(content,note_id,current.user_id,db)
    if updated is not None:
        return updated
    raise HTTPException(status_code=404, detail="Note not found!")


@note_router.delete("/{note_id}", status_code=204)
def delete_note(
    note_id: int,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted = deletenote(note_id, current.user_id, db)

    if deleted == "not_found":
        raise HTTPException(status_code=404, detail="Note not found!")

    return None
