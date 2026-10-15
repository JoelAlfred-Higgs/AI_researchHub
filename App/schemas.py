from pydantic import BaseModel,EmailStr,ConfigDict
from typing import Optional

class CreateUser(BaseModel):
        user_name : str
        email : EmailStr
        password : str
        #EmailStr is a specialized data type in the Pydantic data validation library for Python. It checks that input text matches correct email formatting rules.

class CheckUser(BaseModel):
        user_id : int
        user_name : str
        email : EmailStr

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class CreateNote(BaseModel):
        title : str
        content : str   
        category_id :int

class CreateCategory(BaseModel):
        categ_name : str

class UserResponse(BaseModel):
        user_id : int
        user_name : str
        email : EmailStr
        model_config = ConfigDict(from_attributes =True)

class CategoryResponse(BaseModel):
        categ_id : int
        categ_name : str
        owner_id : int
        model_config = ConfigDict(from_attributes =True)

class NoteResponse(BaseModel):
        note_id : int
        title : str
        content : str
        category_id :int
        owner_id : Optional[int] = None
        model_config = ConfigDict(from_attributes=True)

class UpdateNote(BaseModel):
        title:str
        content :str
        category_id : int

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


        



    