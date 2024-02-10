from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.product_service import ProductService
from app.models.product import Product
from app.schemas import product as product_schema
from app.utils import response_wrapper, GenericResponse
from typing import List

router = APIRouter()
product_service = ProductService()


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a new product
@router.post("/products/", response_model=GenericResponse[product_schema.ProductCreate])
def create_product(product: product_schema.ProductCreate, db: Session = Depends(get_db)):
    try:
        product = product_service.create_product(db, product)
        return response_wrapper("success", "Product Created", product)
    except Exception as e:
        if not e.detail:
            e.detail = response_wrapper("error", "Internal Server Error")
        raise e


# Get a product by ID
@router.get("/products/{product_id}", response_model=GenericResponse[product_schema.Product])
def read_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = product_service.get_product(db, product_id)
        if product is None:
            raise HTTPException(404, response_wrapper(
                "error", "Product Not Found"))
        return response_wrapper("success", "Product Retrieved", product)
    except Exception as e:
        if not e.detail:
            e.detail = response_wrapper("error", "Internal Server Error")
        raise e


# Update a product by ID
@router.put("/products/{product_id}", response_model=GenericResponse[product_schema.ProductUpdate])
def update_product(product_id: int, product: product_schema.ProductUpdate, db: Session = Depends(get_db)):
    try:
        product = product_service.update_product(db, product_id, product)
        return response_wrapper("success", "Product Updated", product)
    except Exception as e:
        if not e.detail:
            e.detail = response_wrapper("error", "Internal Server Error")
        raise e


# Delete a product by ID
@router.delete("/products/{product_id}", response_model=GenericResponse[product_schema.Product])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = product_service.delete_product(db, product_id)
        if product:
            return response_wrapper("success", "Product Deleted", product)
        return response_wrapper("error", "Product Not Found")
    except Exception as e:
        if not e.detail:
            e.detail = response_wrapper("error", "Internal Server Error")
        raise e


# Get all products with pagination and search
@router.get("/products/", response_model=GenericResponse[List[product_schema.Product]])
def read_products(
    page_number: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    search_term: str = None,
    db: Session = Depends(get_db)
):
    try:
        products = product_service.get_products(
            db, page_number=page_number, page_size=page_size, search_term=search_term)
        return response_wrapper("success", "Products Retrieved", products)
    except Exception as e:
        if not e.detail:
            e.detail = response_wrapper("error", "Internal Server Error")
        raise e