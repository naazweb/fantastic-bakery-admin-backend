from pydantic import BaseModel, Field
from typing import Optional


class CategoryBase(BaseModel):
    name: str = Field(..., title="Name",
                      description="The name of the category")
    description: Optional[str] = Field(
        None, title="Description", description="The description of the category")

    class Config:
        orm_mode = True
        error_msg_templates = {
            'value_error.missing': '"Field {field_name}" is required'
        }


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True
