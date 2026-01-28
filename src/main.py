from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import init_db
from .routes.posts import router as post_router
from .routes.categories import router as category_router


app = FastAPI(
    title = settings.app_name,
    debug=settings.debug,
    docs_url='/api/docs',
    redoc_url='/api/redoc'
)

app.mount('/static' , StaticFiles(directory=settings.static_dir), name="static")

app.include_router(post_router)
app.include_router(category_router)

@app.on_event('startup')
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"message" : " welcome to fastapi blogs API", 
            "docs" : "api/docs",
            }

@app.get("/health")
def health_check():
    return {"status" : "все чотка"}