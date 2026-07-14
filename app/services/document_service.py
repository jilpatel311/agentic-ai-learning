import os
import shutil

from fastapi import UploadFile

from app.utils.pdf_parser import PDFParser

UPLOAD_DIR = "uploads"


class DocumentService:

    def upload_document(
        self,
        file: UploadFile
    ):

        os.makedirs(
            UPLOAD_DIR,
            exist_ok=True
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        extracted_text = PDFParser.extract_text(
            file_path
        )

        return {
            "filename": file.filename,
            "text": extracted_text
        }