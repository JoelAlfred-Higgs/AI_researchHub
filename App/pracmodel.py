from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, Field

class Base(DeclarativeBase):
    pass

class Note(Base):
    __tablename__ = "notes"
    
    note_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(String(2000))

class CreateNote(BaseModel):
    note_id : int = Field(gt = 0)#greater than 0, pydantic validation
    title : str = Field(min_length = 1, max_length = 200)
    content : str = Field(min_length = 1, max_length = 2000)

class UpdateNote(BaseModel):
    content:str = Field(min_length = 1, max_length = 2000)

class NoteResponse(BaseModel):
    note_id : int
    title : str
    content : str
    
