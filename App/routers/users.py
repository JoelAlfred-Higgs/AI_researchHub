from fastapi import APIRouter,Depends,HTTPException
from crud import adduser,getuser,checklogin
from schemas import CreateUser,UserResponse,CheckUser,TokenResponse,LoginUser
from DataBase import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from models import Base,User
from security import create_access_token
from dependencies import get_current_user

user_router  = APIRouter()
Base.metadata.create_all(bind = engine) 

@user_router.post("/",status_code=201,response_model=UserResponse)
def add_newuser(user:CreateUser,db:Session = Depends(get_db)):
    res = adduser(user,db)
    if res is None:
        raise HTTPException(status_code=409, detail="User already exists!")
    return res  

"""
@user_router.get("/me",status_code = 200,response_model = CheckUser)
def get_user(user_id:int,db:Session = Depends(get_db)):
    find_user = getuser(user_id,db)
    if find_user is None:
        raise HTTPException(Status_code= 404,detail = "User not Found!")
    return find_user
    """


@user_router.post("/login",status_code = 200,response_model = TokenResponse)
def login_user(user: LoginUser,db:Session = Depends(get_db)):
    find_user = checklogin(user.email,user.password,db)
    if find_user is None:
        raise HTTPException(status_code = 401,detail = "Invalid credentials")
    
    token = create_access_token(find_user.user_id)

    return {"access_token" : token , "token_type":"bearer"}
    

@user_router.get("/me", response_model=UserResponse)
def read_current_user(current_user:User  = Depends(get_current_user)):
    return current_user