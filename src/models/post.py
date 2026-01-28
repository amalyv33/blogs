from sqlalchemy import Column , Integer , String , Text , ForeignKey , DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True , index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category", back_populates="posts")