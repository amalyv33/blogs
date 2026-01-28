import os

class Settings:
    def __init__(self):
        self.app_name = os.getenv("APP_NAME", "FastAPI Blog")
        self.debug = os.getenv("DEBUG", "True").lower() == "true"
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./blog.db")
        self.static_dir = os.getenv("STATIC_DIR", "static")
        self.images_dir = os.getenv("IMAGES_DIR", "static/images")

settings = Settings()