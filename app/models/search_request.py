from pydantic import BaseModel


class SearchRequest(BaseModel):

    session_id: str

    question: str