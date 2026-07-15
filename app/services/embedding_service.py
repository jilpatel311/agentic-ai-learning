from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Generates embeddings for documents and user queries.
    """

    def __init__(self):
        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

    def generate_embeddings(
        self,
        chunks: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple document chunks.
        """

        embeddings = self.model.encode(
            chunks,
            convert_to_numpy=True,
        )

        return embeddings.tolist()

    def generate_query_embedding(
        self,
        query: str,
    ) -> list[float]:
        """
        Generate embedding for a user's question.
        """

        embedding = self.model.encode(
            query,
            convert_to_numpy=True,
        )

        return embedding.tolist()