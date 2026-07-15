import chromadb


class ChromaService:

    def __init__(self):
        """
        Initialize ChromaDB client and collection.
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
        Store document chunks in ChromaDB.
        """

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def similarity_search(
        self,
        query_embedding: list[float],
        top_k: int = 3,
    ):
        """
        Retrieve the most similar document chunks.
        """

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

    def get_all_documents(self):
        """
        Return all stored records.
        Useful for debugging.
        """

        return self.collection.get()