from fastapi import FastAPI

from app.config.settings import settings
from app.api.routes.health import router as health_router
from app.api.routes.documents import router as document_router
from app.api.routes.search import router as search_router
from app.api.routes.chat import router as chat_router

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(document_router)
app.include_router(search_router)
app.include_router(
    chat_router
)