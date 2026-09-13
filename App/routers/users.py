from fastapi import APIRouter,Depends,HTTPException
from crud import adduser,getuser
from schemas import CreateUser,UserResponse,CheckUser
from DataBase import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from models import Base

user_router  = APIRouter()
Base.metadata.create_all(bind = engine) 

@user_router.post("/users",status_code=201,response_model=UserResponse)
def add_newuser(user:CreateUser,db:Session = Depends(get_db)):
    res = adduser(user,db)
    if res is None:
        raise HTTPException(status_code=409, detail="User already exists!")
    return res  

@user_router.get("/users/{user_id}",status_code = 200,response_model = CheckUser)
def get_user(user_id:int,db:Session = Depends(get_db)):
    find_user = getuser(user_id,db)
    if find_user is None:
        raise HTTPException(Status_code= 404,detail = "User not Found!")
    return find_user



