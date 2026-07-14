import os
import shutil

from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.constants.file_constants import (
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE,
)

from app.services.chunking_service import ChunkingService
from app.utils.pdf_parser import PDFParser

UPLOAD_DIR = "uploads"


class DocumentService:

    def __init__(self):
        self.chunking_service = ChunkingService()

    def upload_document(self, file: UploadFile):

        if file.filename is None:
            raise HTTPException(
                status_code=400,
                detail="Filename is missing."
            )

        extension = Path(file.filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Only PDF, DOCX and TXT files are allowed."
            )

        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)

        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File size should not exceed 5 MB."
            )

        os.makedirs(
            UPLOAD_DIR,
            exist_ok=True
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        extracted_text = ""

        if extension == ".pdf":
            extracted_text = PDFParser.extract_text(file_path)

        chunks = self.chunking_service.split_text(extracted_text)

        return {
            "filename": file.filename,
            "total_chunks": len(chunks),
            "chunks": chunks
        }