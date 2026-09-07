from pydantic_core.core_schema import NoInfoWrapValidatorFunction
from pracmodel import Note
def getnote(note_id,db):
 return db.query(Note).filter(Note.note_id == note_id).first()

def addnote(new_note,db):
    if db.query(Note).filter(Note.note_id == new_note.note_id).first():
        return None
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

def updatenote(content,note_id,db):
    un = db.query(Note).filter(Note.note_id == note_id).first()
    if un:
       un.content = content.content
       db.commit()
       db.refresh(un)
       return un
      
    return None
    
def deletenote(note_id,db):
    delete = db.query(Note).filter(Note.note_id == note_id).first()
    if delete is not None:
       db.delete(delete)
       db.commit()
       return 1
    return None