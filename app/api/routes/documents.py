from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from app.services.document_service import DocumentService


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

service = DocumentService()


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...)
):

    return service.upload_document(
        file
    )