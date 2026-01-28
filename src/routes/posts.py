from fastapi import APIRouter , Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.post_services import PostServices
from ..schemas.post import PostResponse , PostListReponse

router = APIRouter(
    prefix="/api/posts",
    tags=['posts']
)

@router.get("", response_model= PostListReponse,status_code=status.HTTP_200_OK)
def get_posts(db : Session = Depends(get_db)):
    service = PostServices(db)
    return service.get_all()

@router.get("/{post_id}", response_model= PostResponse, status_code=status.HTTP_200_OK)
def get_by_category_id( post_id : int,db : Session = Depends(get_db)):
    service = PostServices(db)
    return service.get_post_by_id(post_id)

@router.get("/category/{category_id}", response_model=PostListReponse, status_code=status.HTTP_200_OK)
def get_post_by_category(category_id : int , db : Session = Depends(get_db)):
    service= PostServices(db)
    return service.get_post_by_category(category_id)