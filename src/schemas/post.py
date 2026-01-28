from pydantic import BaseModel , Field
from datetime import datetime
from typing import Optional
from .category import CategoryResponse

class PostBase(BaseModel):
    name : str = Field(... ,min_lenght=5 , max_lenght=100, description="Название поста")
    description : Optional[str] = Field(None, description='Описание поста')
    
    category_id : int = Field(..., description="Индификатор категории")
    image_url : Optional[str] = Field(None,description="Фотография для поста")

class PostCreate(PostBase):
    pass

class PostResponse(BaseModel):
    id : int 
    name : str
    description : Optional[str]
    category_id : int
    image_url : Optional[str]
    created_at : datetime
    category : CategoryResponse = Field(..., description="Категория продукта")

    class Config:
        form_attributes = True

class PostListReponse(BaseModel):
    posts : list[PostResponse]
    total : int = Field(..., description="Количество постов")