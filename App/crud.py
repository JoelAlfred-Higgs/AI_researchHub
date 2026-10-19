
from models import Category, Note, User
from security import hash_password, verify_password

def getnote(note_id, db, owner_id=None):
    query = db.query(Note).filter(Note.note_id == note_id)
    if owner_id is not None:
        query = query.filter(Note.owner_id == owner_id)
    return query.first()

def getallnotes(db,owner_id):
    return db.query(Note).filter(Note.owner_id  == owner_id).all()

def getallnotes_bycategory(db,owner_id,categ_id):
    return db.query(Note).filter(Note.owner_id == owner_id,Note.category_id == categ_id).all()

def getcategory_byuser(db,owner_id):
    return db.query(Category).filter(Category.owner_id == owner_id).all()

def addnote(new_note,db):
    category = db.query(Category).filter(
        Category.categ_id == new_note.category_id,
        Category.owner_id == new_note.owner_id,
    ).first()
    if category is None:
        return None
    try:
        db.add(new_note)
        db.commit()
        db.refresh(new_note)
        return new_note
    except Exception:
        db.rollback()
        raise

def updatenote(content,note_id,current_userid,db):
    category_exist = db.query(Category).filter(
        Category.categ_id == content.category_id,
        Category.owner_id == current_userid,
    ).first()
    if category_exist is None:
        return None
    note_exist = db.query(Note).filter(
        Note.note_id == note_id,
        Note.owner_id == current_userid,
    ).first()
    if note_exist is None:
        return None

    note_exist.title = content.title
    note_exist.content = content.content
    note_exist.category_id = content.category_id
    try:
        db.commit()
        db.refresh(note_exist)
        return note_exist
    except Exception:
        db.rollback()
        raise
      
def deletenote(note_id, owner_id, db):
    delete = db.query(Note).filter(Note.note_id == note_id,Note.owner_id == owner_id).first()

    if delete is None:
        return "not_found"
    try:
     db.delete(delete)
     db.commit()
     return "deleted"
    except Exception:
        db.rollback()
        raise

def adduser(user, db):
    if db.query(User).filter((User.user_name == user.user_name ) | (User.email == user.email)).first():
        return None
    hashed_password = hash_password(user.password)

    new_user = User(user_name=user.user_name,email=user.email,password=hashed_password)
    try:
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     return new_user
    except Exception:
        db.rollback()
        raise

def getuser(user_id,db):
    return db.query(User).filter(User.user_id == user_id).first()

def checklogin(email,pwd,db):
    find_user = db.query(User).filter(User.email == email).first()
    if find_user is None:
        return None
    if verify_password(pwd,find_user.password):
        return find_user
    return None

def addcategory(new_category,db):
    user_exist = db.query(User).filter(User.user_id == new_category.owner_id).first()
    if user_exist is None:
        return None

    try:
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except Exception:
        db.rollback()
        raise

def getcategory(category_id,db):
    return db.query(Category).filter(Category.categ_id == category_id).first()

def updatecategory(category_id,owner_id,new_categ,db):
   check_categ = db.query(Category).filter(
       Category.categ_id == category_id,
       Category.owner_id == owner_id,
   ).first()
   if check_categ is None:
       return None
   check_categ.categ_name = new_categ.categ_name
   try:
     db.commit()
     db.refresh(check_categ)
     return check_categ
   except Exception:
    db.rollback()
    raise

  

def deletecategory(category_id, owner_id, db):
    del_categ = db.query(Category).filter(
        Category.categ_id == category_id,
        Category.owner_id == owner_id,
    ).first()

    if del_categ is None:
        return "not_found"
    notes_exist = db.query(Note).filter(Note.category_id == category_id).first()
    if notes_exist is not None:
        return "has_notes"
    try:
        db.delete(del_categ)
        db.commit()
        return "deleted"
    except Exception:
        db.rollback()
        raise
