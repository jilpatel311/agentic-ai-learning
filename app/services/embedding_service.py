from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Generates vector embeddings for document chunks.
    """

    def __init__(self):
        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

    def generate_embeddings(
        self,
        chunks: list[str]
    ) -> list[list[float]]:
        """
        Convert text chunks into vector embeddings.
        """
        embeddings = self.model.encode(
            chunks,
            convert_to_numpy=True
        )

        return embeddings.tolist()