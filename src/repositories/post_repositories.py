from sqlalchemy.orm import Session , joinedload
from typing import List , Optional
from ..models.post import Post
from ..schemas.post import PostCreate

class PostRepositories:
    def __init__(self, db : Session) :
            self.db = db

    def get_all(self) -> List[Post]:
          return self.db.query(Post).options(joinedload(Post.category)).all()
    
    def get_by_id(self, post_id : int) -> Optional[Post]:
          return (
                self.db.query(Post)
                .options(joinedload(Post.category))
                .filter(Post.id == post_id)
                .first()
          )
    
    def get_by_category(self , category_id: int) -> List[Post]:
          return(
                self.db.query(Post)
                .options(joinedload(Post.category))
                .filter(Post.category_id == category_id)
                .all()
          )
    
    def create(self, post_date : PostCreate) -> Post:
          db_post = Post(**post_date.model_dump())
          self.db.add(db_post)
          self.db.commit()
          self.db.refresh(db_post)
          return db_post