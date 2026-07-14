from fastapi import APIRouter, UploadFile, File

from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

document_service = DocumentService()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(..., description="PDF file to upload")
):
    """
    Upload a PDF document for processing.
    
    - **file**: The PDF file to upload
    """
    return document_service.upload_document(file)