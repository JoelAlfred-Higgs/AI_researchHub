from pracmodel import Note
def getnote(note_id,db):
 return db.query(Note).filter(Note.note_id == note_id).first()

def addnote(new_note,db):
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

def updatenote(Note,content,note_id,db):
    un = db.query(Note).filter(Note.note_id == note_id).first()
    if un:
       un.content = content
       db.commit()
       return un
      
    return None
    
def deletenote(Note,note_id,db):
    delete = db.query(Note).filter(Note.note_id == note_id).first()
    db.delete(delete)
    db.commit()
    return 1