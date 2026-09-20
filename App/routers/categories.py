from crud import addcategory,getcategory,updatecategory,deletecategory
from DataBase import engine,get_db
from models import Category,Base
from schemas import CreateCategory, CategoryResponse
from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session

categ_router = APIRouter()
Base.metadata.create_all(bind = engine) #creates table for categories

@categ_router.post("/",response_model = CategoryResponse,status_code = 201)
def add_category(categ:CreateCategory,db:Session = Depends(get_db)):
    res = addcategory(categ,db)
    if res is None:
        raise HTTPException (status_code = 404 , detail ="Owner not found!")
    return res

@categ_router.get("/{categ_id}",response_model = CategoryResponse,status_code = 200)
def get_category(categ_id:int,db:Session = Depends(get_db)):
    find_category = getcategory(categ_id,db)
    if find_category is None:
        raise HTTPException(status_code=404,detail="Category not found!")
    return find_category

@categ_router.put("/{categ_id}",response_model = CategoryResponse,status_code = 200)
def update_category(categ_id:int,update_category:CategoryResponse,db:Session = Depends(get_db)):
    updated = updatecategory(categ_id,update_category,db)
    if updated is None:
        raise HTTPException(status_code=404,detail="Category not found!")
    return updated

@categ_router.delete("/{categ_id}",response_model = CategoryResponse,status_code = 200)
def delete_category(categ_id :int,db:Session = Depends(get_db)):
    deleted_categ = deletecategory(categ_id,db)
    if deleted_categ is None:
        raise HTTPException(status_code=404,detail="Category not found!")
    return deleted_categ



