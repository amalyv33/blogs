from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name : str = "FastAPI Blog"
    debug : bool = True
    database_url : str = "sqlite:///./blog.db"
    static_dir : str = "static"
    images_dir : str = "static/images"

    class Config:
        env_file = ".env"

settings = Settings()