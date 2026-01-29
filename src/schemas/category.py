from pydantic import BaseModel, Field
from typing import List

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Название категории")
    slug: str = Field(..., min_length=3, max_length=100, description="Урл по имени категории")

class CategoryCreate(CategoryBase):
    pass 

class CategoryResponse(CategoryBase):
    id: int = Field(..., description="Уникальный индификатор")

    class Config:
        from_attributes = True