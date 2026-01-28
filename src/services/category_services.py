from sqlalchemy.orm import Session
from typing import List
from ..repositories.category_repositories import CategoryRepositories
from ..schemas.category import CategoryResponse , CategoryCreate
from fastapi import HTTPException , status

class CategoryServices:
    def __init__(self, db: Session):
        self.repository = CategoryRepositories(db)

    def get_all_categories(self) -> List[CategoryResponse]:
        categories = self.repository.get_all()
        return [CategoryResponse.model_validate(cat) for cat in categories] 
    
    def get_category_by_id(self, category_id) -> CategoryResponse:
        category = self.repository.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Категория с {category_id}  не найдена')
        return CategoryResponse.model_validate(category)
    
    def create_category(self , category_date: CategoryCreate) -> CategoryResponse:
        category = self.repository.create(category_date)
        return CategoryResponse.model_validate(category)