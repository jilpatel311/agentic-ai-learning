from fastapi import APIRouter

from app.schemas.chat import ChatRequest
from app.services.agent_service import AgentService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

agent_service = AgentService()


@router.post("/")
async def chat(
    request: ChatRequest,
):

    return agent_service.process_question(
        request.question
    )