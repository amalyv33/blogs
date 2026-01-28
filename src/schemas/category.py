from pydantic import BaseModel , Field

class CategoryBase(BaseModel):
    name : str = Field(... ,min_lenght=5 , max_lenght=100, description="Название категории")
    slug : str = Field(..., min_leght=5, max_leght=100,description="Урл по имени категории")

class CategoryCreate(CategoryBase):
    pass 

class CategoryResponse(CategoryBase):
    id : int = Field(..., description="Уникальный индификатор")

    class Config:
        form_attributes = True
