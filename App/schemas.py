
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional


class CreateUser(BaseModel):
    user_name: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class CheckUser(BaseModel):
    user_id: int
    user_name: str
    email: EmailStr


class UpdateCategory(BaseModel):
    categ_name: str = Field(min_length=1, max_length=100)


class LoginUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class CreateNote(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=10000)
    category_id: int = Field(gt=0)


class CreateCategory(BaseModel):
    categ_name: str = Field(min_length=1, max_length=100)


class UserResponse(BaseModel):
    user_id: int
    user_name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class CategoryResponse(BaseModel):
    categ_id: int
    categ_name: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class NoteResponse(BaseModel):
    note_id: int
    title: str
    content: str
    category_id: int
    owner_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class UpdateNote(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=10000)
    category_id: int = Field(gt=0)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
