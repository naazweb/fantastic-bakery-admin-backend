from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas import category as category_schema
from sqlalchemy import select, or_
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page, Params


class CategoryService:
    def create_category(self, db: Session, category: category_schema.CategoryCreate) -> Category:
        # Convert Pydantic CategoryCreate model to SQLAlchemy Category model
        db_category = Category(
            name=category.name,
            description=category.description,
        )
        # Add the SQLAlchemy Category model to the session
        db.add(db_category)
        # Commit the transaction to save changes to the database
        db.commit()
        # Refresh the SQLAlchemy Category model to update its state from the database
        db.refresh(db_category)
        # Return the SQLAlchemy Category model
        return db_category

    def update_category(self, db: Session, category_id: int, category_update: category_schema.CategoryUpdate) -> Category:
        # get the category by id
        db_category = self.get_category(db, category_id)
        if db_category:
            # Prepare a dictionary with the fields to update
            update_data = category_update.dict(exclude_unset=True)
            # Update the category in the database
            db.query(Category).filter(Category.id ==
                                      category_id).update(update_data)
            # Commit the changes to the database
            db.commit()
            # Refresh the db_category object to reflect the changes from the database
            db.refresh(db_category)
            return db_category
        return None

    def delete_category(self, db: Session, category_id: int) -> Category:
        # get the category by id
        category = self.get_category(db, category_id)
        if category:
            # delete the category if exists
            db.delete(category)
            db.commit()
            return category
        return None

    def get_category(self, db: Session, category_id: int) -> Category:
        # filter by category id
        return db.query(Category).filter(Category.id == category_id).first()

    def get_categories(
        self,
        db: Session,
        page_number: int = 1,
        page_size: int = 10,
        search_term: str = None
    ) -> Page[Category]:
        # query to get all
        query = db.query(Category)
        if search_term:
            search_expr = f"%{search_term}%"
            # if search_term exists -> filter by name or description
            query = query.filter(
                or_(
                    Category.name.ilike(search_expr),
                    Category.description.ilike(search_expr)
                )
            )
        # apply pagination
        paginated_categories = paginate(
            query, params=Params(size=page_size, page=page_number))
        return paginated_categories
