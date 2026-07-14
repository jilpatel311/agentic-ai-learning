import chromadb


class ChromaService:

    def __init__(self):
        """
        Initialize a persistent ChromaDB client.
        """
        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="company_documents"
        )

    def add_embeddings(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:
        """
        Store document chunks and embeddings.
        """

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def get_all_documents(self):
        """
        Fetch every stored record.
        """

        return self.collection.get()

    def similarity_search(
        self,
        embedding: list[float],
        top_k: int = 3,
    ):
        """
        Search the nearest vectors.
        """

        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )