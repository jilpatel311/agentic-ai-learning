import uuid

from pathlib import Path

from fastapi import HTTPException

from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.chroma_service import ChromaService

from app.utils.pdf_parser import PDFParser


class DocumentIngestionService:

    def __init__(self):
        self.chunking_service = ChunkingService()
        self.embedding_service = EmbeddingService()
        self.chroma_service = ChromaService()

    def ingest_document(
        self,
        file_path: str,
        filename: str,
    ):

        extension = Path(file_path).suffix.lower()

        extracted_text = ""

        if extension == ".pdf":
            extracted_text = PDFParser.extract_text(file_path)

        # Validate extracted text
        if not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the uploaded document."
            )

        # Split into chunks
        chunks = self.chunking_service.split_text(extracted_text)

        # Generate embeddings
        embeddings = self.embedding_service.generate_embeddings(chunks)

        # Generate unique IDs for every chunk
        ids = [
            str(uuid.uuid4())
            for _ in chunks
        ]

        # Metadata
        metadatas = [
            {
                "filename": filename,
                "chunk_index": index,
                "source": "pdf"
            }
            for index in range(len(chunks))
        ]

        # Store in ChromaDB
        self.chroma_service.add_embeddings(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        return {
            "filename": filename,
            "chunks_created": len(chunks),
            "embeddings_created": len(embeddings),
        }