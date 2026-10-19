from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import addcategory, updatecategory, deletecategory, getcategory_byuser
from DataBase import get_db
from dependencies import get_current_user
from models import Category, User
from schemas import CreateCategory, CategoryResponse, UpdateCategory

categ_router = APIRouter()


@categ_router.post("/", response_model=CategoryResponse, status_code=201)
def add_category(
    categ: CreateCategory,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_cat = Category(
        owner_id=current_user.user_id,
        categ_name=categ.categ_name,
    )

    result = addcategory(new_cat, db)

    if result is None:
        raise HTTPException(
            status_code=500,
            detail="Unable to create category",
        )

    return result


@categ_router.get("/", response_model=list[CategoryResponse], status_code=200)
def get_category(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Returning an empty list is valid when no categories exist.
    return getcategory_byuser(db, current_user.user_id)


@categ_router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=200,
)
def update_category(
    category_id: int,
    update_categ: UpdateCategory,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    updated = updatecategory(
        category_id,
        current.user_id,
        update_categ,
        db,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found!",
        )

    return updated


@categ_router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = deletecategory(category_id, current.user_id, db)

    if result == "not_found":
        raise HTTPException(
            status_code=404,
            detail="Category not found!",
        )

    if result == "has_notes":
        raise HTTPException(
            status_code=409,
            detail="Cannot delete category with notes!",
        )

    return None