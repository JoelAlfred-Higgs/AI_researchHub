
from models import Note,User,Category
from security import hash_password,verify_password

def getnote(note_id,db):
 return db.query(Note).filter(Note.note_id == note_id).first()

def getallnotes(db,owner_id):
    return db.query(Note).filter(Note.owner_id  == owner_id).all()

def getallnotes_bycategory(db,owner_id,categ_id):
    return db.query(Note).filter(Note.owner_id == owner_id,Note.category_id == categ_id).all()

def getcategory_byuser(db,owner_id):
    return db.query(Category).filter(Category.owner_id == owner_id).all()

def addnote(new_note,db):
    if db.query(Note).filter(Note.note_id == new_note.note_id).first():
        return None
    if db.query(Category).filter(Category.categ_id == new_note.category_id).first() is None:
        return None
    if db.query(User).filter(User.user_id == new_note.owner_id).first() is None:
        return None
    if db.query(Category).filter(Category.owner_id == new_note.owner_id,Category.categ_id  == new_note.category_id).first() is None:
        return None
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

def updatenote(content,note_id,db):
    category_exist = db.query(Category).filter(Category.categ_id == content.category_id).first()
    if category_exist is None:
        return None
    note_exist = db.query(Note).filter(Note.note_id == note_id).first()
    if note_exist is None:
        return None  
    owner_exist = db.query(Category).filter(Category.owner_id == note_exist.owner_id,Category.categ_id == content.category_id).first()
    if owner_exist is None:
        return None
    if note_exist:
       note_exist.title = content.title
       note_exist.content = content.content
       note_exist.category_id = content.category_id
       db.commit()
       db.refresh(note_exist)
       return note_exist
    else:
        return None
      
def deletenote(note_id, owner_id, db):
    delete = db.query(Note).filter(Note.note_id == note_id).first()

    if delete is None:
        return None

    if delete.owner_id != owner_id:
        return None

    db.delete(delete)
    db.commit()
    return 1


def adduser(user, db):
    if db.query(User).filter((User.user_name == user.user_name) | (User.email == user.email)).first():
        return None
    hashed_password = hash_password(user.password)

    new_user = User(user_name=user.user_name,email=user.email,password=hashed_password)
    db.add(new_user)    
    db.commit()
    db.refresh(new_user)
    return new_user

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
    user_exist =  db.query(User).filter(User.user_id == new_category.owner_id).first() 
    if user_exist is None:
        return None    
    new_category = Category(categ_name = new_category.categ_name,owner_id = new_category.owner_id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def getcategory(category_id,db):
    return db.query(Category).filter(Category.categ_id == category_id).first()

def updatecategory(category_id,owner_id,new_categ,db):
   check_categ = db.query(Category).filter(Category.categ_id == category_id).first()
   if check_categ is None:
       return None
   if check_categ.owner_id == owner_id:
        check_categ.categ_name = new_categ.categ_name
        db.commit()
        db.refresh(check_categ) 
        return check_categ 
   return None 

def deletecategory(category_id, owner_id, db):
    del_categ = db.query(Category).filter(Category.categ_id == category_id).first()

    if del_categ is None:
        return None
    if del_categ.owner_id != owner_id:
        return None
    notes_exist = db.query(Note).filter(Note.category_id == category_id).first()
    if notes_exist is not None:
        return None
    db.delete(del_categ)
    db.commit()

    return 1
