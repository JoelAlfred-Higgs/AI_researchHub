from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel

class Base(DeclarativeBase):
    pass

class Note(Base):
    __tablename__ = "notes"
    
    note_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(String(2000))

class CreateNote(BaseModel):
    note_id : int
    title : str
    content : str

class UpdateNote(BaseModel):
    content:str

class NoteResponse(BaseModel):
    note_id : int
    title : str
    content : str
    
