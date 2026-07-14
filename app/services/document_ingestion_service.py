from pathlib import Path

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
            extracted_text = PDFParser.extract_text(
                file_path
            )

        chunks = self.chunking_service.split_text(
            extracted_text
        )

        embeddings = self.embedding_service.generate_embeddings(
            chunks
        )

        ids = [
            f"{filename}_{index}"
            for index in range(len(chunks))
        ]

        metadatas = [
            {
                "filename": filename,
                "chunk": index
            }
            for index in range(len(chunks))
        ]

        self.chroma_service.add_embeddings(

            ids=ids,

            documents=chunks,

            embeddings=embeddings,

            metadatas=metadatas
        )

        return {

            "filename": filename,

            "chunks_created": len(chunks),

            "embeddings_created": len(embeddings)

        }