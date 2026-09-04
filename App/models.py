from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Text,ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()
class User(Base): #stores the details of the user
    __tablename__ = "users"
    user_id = Column(Integer,primary_key=True)
    user_name = Column(String(30),nullable = False,unique = True)
    email = Column(String(50),nullable = False,unique = True)
    category = relationship("Category",back_populates = "user")
    notes  = relationship("Note",back_populates = "user")
    
    #Back populates-link two object models together, update one object and linked object gets updated

class Category(Base): #holds the category of notes
    __tablename__ = "categories"
    categ_id = Column(Integer,primary_key = True,index = True)
    categ_name = Column(String(100),nullable = False)
    owner_id = Column(Integer,ForeignKey = "users.user_id")
    user = relationship("User",back_populates = "category")
    notes = relationship("Note",back_populates = "category")

class Notes(Base):
    __tablename__ = "notes" # core unit and contains the main content
    note_id  = Column(Integer,primary_key = True,index = True)
    title = Column(String(50),nullable = False)
    content  = Column(Text,nullable = False)
    owner_id = Column(Integer,ForeignKey = "users.user_id")
    category_id = Column(Integer,ForeignKey = "categories.categ_id")
    category = relationship("Category",back_populates = "notes")
    user = relationship("User",back_populates = "notes")
