from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.category_service import CategoryService
from app.models.category import Category
from app.schemas import category as category_schema
from app.utils import response_wrapper, GenericResponse
from typing import List
from fastapi_pagination import Page

router = APIRouter()
category_service = CategoryService()


# Dependency to get a database session
def get_db():
    """
    Dependency to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a new category
@router.post("/categories/", response_model=GenericResponse[category_schema.CategoryCreate], tags=["Categories"])
def create_category(category: category_schema.CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new category.

    :param category: The details of the category to create.
    :param db: Database session dependency.

    :return: The created category.
    """
    try:
        created_category = category_service.create_category(db, category)
        return response_wrapper("success", "Category Created", created_category)
    except Exception as e:
        if not hasattr(e, 'detail'):
            e.detail = response_wrapper("error", "Internal Server Error")
        raise e


# Update a category by ID
@router.put("/categories/{category_id}", response_model=GenericResponse[category_schema.CategoryUpdate], tags=["Categories"])
def update_category(category_id: int, category: category_schema.CategoryUpdate, db: Session = Depends(get_db)):
    """
    Update a category by its ID.

    :param category_id: The ID of the category to update.
    :param category: The details of the category to update.
    :param db: Database session dependency.

    :return: The updated category.
    """
    try:
        category = category_service.update_category(
            db, category_id, category)
        if category:
            return response_wrapper("success", "Category Updated", category)
        raise HTTPException(404, response_wrapper(
            "error", "Category Not Found"))
    except Exception as e:
        if not hasattr(e, 'detail'):
            e.detail = response_wrapper("error", "Internal Server Error")
        raise e


# Delete a category by ID
@router.delete("/categories/{category_id}", response_model=GenericResponse[category_schema.Category], tags=["Categories"])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    Delete a category by its ID.

    :param category_id: The ID of the category to delete.
    :param db: Database session dependency.

    :return: The deleted category.
    """
    try:
        category = category_service.delete_category(db, category_id)
        if category:
            return response_wrapper("success", "Category Deleted", category)
        raise HTTPException(404, response_wrapper(
            "error", "Category Not Found"))
    except Exception as e:
        if not hasattr(e, 'detail'):
            e.detail = response_wrapper("error", "Internal Server Error")
        raise e


# Get a category by ID
@router.get("/categories/{category_id}", response_model=GenericResponse[category_schema.Category], tags=["Categories"])
def read_category(category_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a category by its ID.

    :param category_id: The ID of the category to retrieve.
    :param db: Database session dependency.

    :return: The retrieved category.
    """
    try:
        category = category_service.get_category(db, category_id)
        if category is None:
            raise HTTPException(404, response_wrapper(
                "error", "Category Not Found"))
        return response_wrapper("success", "Category Retrieved", category)
    except Exception as e:
        if not hasattr(e, 'detail'):
            e.detail = response_wrapper("error", "Internal Server Error")
        raise e


# Get all categories with pagination and search
@router.get("/categories/", response_model=GenericResponse[Page[category_schema.Category]], tags=["Categories"])
def read_categories(
    page_number: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    search_term: str = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve all categories with pagination and optional search filtering.

    :param page_number: The page number for pagination (default: 1).
    :param page_size: The page size for pagination (default: 10).
    :param search_term: Optional search term to filter categories by name or description.
    :param db: Database session dependency.

    :return: Paginated list of categories.
    """
    try:
        categories = category_service.get_categories(
            db, page_number=page_number, page_size=page_size, search_term=search_term)
        return response_wrapper("success", "Categories Retrieved", categories)
    except Exception as e:
        if not hasattr(e, 'detail'):
            e.detail = response_wrapper("error", "Internal Server Error")
        raise e
