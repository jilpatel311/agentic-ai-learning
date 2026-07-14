import os
import shutil

from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.constants.file_constants import (
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE,
)

from app.services.document_ingestion_service import (
    DocumentIngestionService,
)

UPLOAD_DIR = "uploads"


class DocumentService:

    def __init__(self):
        self.document_ingestion_service = DocumentIngestionService()

    def upload_document(self, file: UploadFile):

        # Validate filename
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Filename is missing."
            )

        # Validate extension
        extension = Path(file.filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Only PDF, DOCX and TXT files are allowed."
            )

        # Validate file size
        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)

        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File size should not exceed 5 MB."
            )

        # Create uploads directory if needed
        os.makedirs(
            UPLOAD_DIR,
            exist_ok=True
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        # Start AI ingestion pipeline
        result = self.document_ingestion_service.ingest_document(
            file_path=file_path,
            filename=file.filename
        )

        return {
            "message": "Document processed successfully.",
            **result
        }