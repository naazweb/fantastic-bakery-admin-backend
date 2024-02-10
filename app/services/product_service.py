from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas import product as product_schema
from sqlalchemy import select, or_
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page, Params


class ProductService:
    def create_product(self, db: Session, product: product_schema.ProductCreate) -> Product:
        # Convert Pydantic ProductCreate model to SQLAlchemy Product model
        db_product = Product(
            name=product.name,
            description=product.description,
            quantity=product.quantity,
            price=product.price
        )
        # Add the SQLAlchemy Product model to the session
        db.add(db_product)
        # Commit the transaction to save changes to the database
        db.commit()
        # Refresh the SQLAlchemy Product model to update its state from the database
        db.refresh(db_product)
        # Return the SQLAlchemy Product model
        return db_product

    def get_product(self, db: Session, product_id: int) -> Product:
        return db.query(Product).filter(Product.id == product_id).first()

    def update_product(self, db: Session, product_id: int, product_update: product_schema.ProductUpdate) -> Product:
        db_product = self.get_product(db, product_id)
        if db_product:
            # Prepare a dictionary with the fields to update
            update_data = product_update.dict(exclude_unset=True)
            # Update the product in the database
            db.query(Product).filter(Product.id ==
                                     product_id).update(update_data)
            # Commit the changes to the database
            db.commit()
            # Refresh the db_product object to reflect the changes from the database
            db.refresh(db_product)
            return db_product
        return None

    def delete_product(self, db: Session, product_id: int) -> Product:
        product = self.get_product(db, product_id)
        if product:
            db.delete(product)
            db.commit()
            return product
        return None

    def get_products(
        self,
        db: Session,
        page_number: int = 1,
        page_size: int = 10,
        search_term: str = None
    ) -> Page[Product]:
        query = db.query(Product)
        # Apply search filter if search_term provided
        if search_term:
            search_expr = f"%{search_term}%"
            query = query.filter(
                or_(
                    Product.name.ilike(search_expr),
                    Product.description.ilike(search_expr)
                )
            )
        # Apply pagination
        return paginate(db, query, params=Params(size=page_size, page=page_number))
