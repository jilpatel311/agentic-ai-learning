from fastapi import FastAPI

from app.config.settings import settings
from app.api.routes.health import router as health_router
from app.api.routes.documents import router as document_router

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(document_router)