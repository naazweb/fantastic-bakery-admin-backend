from pydantic import BaseModel, Field
from typing import Optional


class ProductBase(BaseModel):
    name: str = Field(..., title="Name", description="The name of the product")
    description: Optional[str] = Field(
        None, title="Description", description="The description of the product")
    quantity: int = Field(1, title="Quantity",
                          description="The quantity of the product")
    price: float = Field(..., title="Price",
                         description="The price of the product")

    class Config:
        orm_mode = True
        error_msg_templates = {
            'value_error.missing': '"{field_name}" is required'
        }


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None

    class Config:
        orm_mode = True


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
