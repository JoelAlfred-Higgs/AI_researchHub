from schemas import UpdateCategory
from crud import addcategory,getcategory,updatecategory,deletecategory,getcategory_byuser
from DataBase import engine,get_db
from models import Category,Base
from schemas import CreateCategory, CategoryResponse
from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from dependencies import get_current_user
from models import User

categ_router = APIRouter()
Base.metadata.create_all(bind = engine) #creates table for categories

@categ_router.post("/",response_model = CategoryResponse,status_code = 201)
def add_category(categ:CreateCategory,current_user:User = Depends(get_current_user),db:Session = Depends(get_db)):
    
    #create a new category
    new_cat = Category(owner_id = current_user.user_id,categ_name = categ.categ_name)
    
    #add category to database
    res = addcategory(new_cat,db)

    #check if owner exists
    if res is None:
        raise HTTPException (status_code = 404 , detail ="Owner not found!")
        
    #return the new category
    return res

@categ_router.get("/",response_model = list[CategoryResponse],status_code = 200)
def get_category(current_user:User = Depends(get_current_user),db:Session = Depends(get_db)):
    categ = getcategory_byuser(db,current_user.user_id)
    if categ is None:
        raise HTTPException(status_code=404,detail="Category not found!")
    return categ

@categ_router.put("/{category_id}",response_model = CategoryResponse,status_code = 200)
def update_category(category_id:int,update_categ:UpdateCategory,current:User = Depends(get_current_user),db:Session = Depends(get_db)):
    updated = updatecategory(category_id,current.user_id,update_categ,db)
    if updated is None:
        raise HTTPException(status_code=404,detail="Category not found!")
    return updated

@categ_router.delete("/{category_id}",status_code = 200)
def delete_category(category_id:int,current:User = Depends(get_current_user),db:Session = Depends(get_db)):
    deleted_categ = deletecategory(category_id,current.user_id,db)
    if deleted_categ == "not_found":
        raise HTTPException(status_code=404,detail="Category not found!")

    if deleted_categ == "forbidden":
        raise HTTPException(status_code=404,detail="Access Denied!")

    if deleted_categ == "has_notes":
        raise HTTPException(status_code = 409,detail = "Cannot delete category with notes!")
        
    return "deleted"


@categ_router.get("/mine",response_model = list[CategoryResponse],status_code = 200)
def get_category_byuser(current:User = Depends(get_current_user),db:Session = Depends(get_db)):
    categ = getcategory_byuser(db,current.user_id)

    return categ        

    




