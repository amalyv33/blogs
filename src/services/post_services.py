from sqlalchemy.orm import Session
from typing import List
from ..repositories.post_repositories import PostRepositories
from ..repositories.category_repositories import CategoryRepositories
from ..schemas.post import PostListReponse , PostResponse, PostCreate
from fastapi import HTTPException , status

class PostServices:
    def __init__(self, db: Session):
        self.repository = PostRepositories(db)
        self.category_repository = CategoryRepositories(db)

    def get_all(self):
        posts = self.repository.get_all()
        post_response = [PostListReponse.model_validate(post) for post in posts]
        return PostListReponse(posts=post_response, total=len(post_response))
    
    def get_post_by_id(self ,post_id : int) -> PostResponse:
        post = self.repository.get_by_id(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пост с {post_id} не найден")
        return PostResponse.model_validate(post)    
    
    def get_post_by_category(self,category_id) -> PostResponse:
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Категория с {category_id} , не найден')
        posts = self.repository.get_by_category(category_id) 
        post_response = [PostResponse.model_validate(post) for post in posts]
        return PostListReponse(posts=post_response, total=len(post_response))
    
    def create_post(self, post_data : PostCreate) -> PostResponse:
        category = self.category_repository.get_by_id(post_data.category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Категория с {category_id} , не найден')
        post = self.repository.create(post_data)
        return PostResponse.model_validate(post)