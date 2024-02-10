from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

    # Define a foreign key relationship with Category
    category_id = Column(Integer, ForeignKey("categories.id"))

    # Establish a many-to-one relationship with Category
    category = relationship("Category", back_populates="products")
