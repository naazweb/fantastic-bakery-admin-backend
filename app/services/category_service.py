from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas import category as category_schema
from sqlalchemy import select, or_
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page, Params


class CategoryService:
    def create_category(self, db: Session, category: category_schema.CategoryCreate) -> Category:
        db_category = Category(
            name=category.name,
            description=category.description,
        )
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    def get_category(self, db: Session, category_id: int) -> Category:
        return db.query(Category).filter(Category.id == category_id).first()

    def update_category(self, db: Session, category_id: int, category_update: category_schema.CategoryUpdate) -> Category:
        db_category = self.get_category(db, category_id)
        if db_category:
            update_data = category_update.dict(exclude_unset=True)
            db.query(Category).filter(Category.id ==
                                      category_id).update(update_data)
            db.commit()
            db.refresh(db_category)
            return db_category
        return None

    def delete_category(self, db: Session, category_id: int) -> Category:
        category = self.get_category(db, category_id)
        if category:
            db.delete(category)
            db.commit()
            return category
        return None

    def get_categories(
        self,
        db: Session,
        page_number: int = 1,
        page_size: int = 10,
        search_term: str = None
    ) -> Page[Category]:
        query = db.query(Category)
        if search_term:
            search_expr = f"%{search_term}%"
            query = query.filter(
                or_(
                    Category.name.ilike(search_expr),
                    Category.description.ilike(search_expr)
                )
            )
        return paginate(query, params=Params(size=page_size, page=page_number))
