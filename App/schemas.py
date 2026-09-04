from pydantic import BaseModel,EmailStr

class CreateUser(BaseModel):
        user_name : str
        email : EmailStr
        #EmailStr is a specialized data type in the Pydantic data validation library for Python. It checks that input text matches correct email formatting rules.

class CheckUser(BaseModel):
        user_id : int
        user_name : str
        email : EmailStr

class CreateNote(BaseModel):
        title : str
        content : str
        categ_id :int


        



    