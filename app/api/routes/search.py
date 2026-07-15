from fastapi import APIRouter

from app.models.search_request import SearchRequest
from app.services.search_service import SearchService

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)

search_service = SearchService()


@router.post("/")
async def search(
    request: SearchRequest,
):
    return search_service.search(
        session_id=request.session_id,
        question=request.question,
    )