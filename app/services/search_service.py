from app.services.embedding_service import EmbeddingService
from app.services.chroma_service import ChromaService
from app.services.groq_service import GroqService
from app.services.conversation_memory_service import (
    ConversationMemoryService,
)


class SearchService:

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.chroma_service = ChromaService()

        self.groq_service = GroqService()

        self.memory_service = ConversationMemoryService()

    def search(
        self,
        session_id: str,
        question: str,
    ):

        # Get previous conversation
        conversation_history = self.memory_service.get_messages(
            session_id
        )

        # Rewrite question using conversation history
        rewritten_question = self.groq_service.rewrite_question(
            question=question,
            conversation_history=conversation_history,
        )

        print("=" * 70)
        print(f"Original Question : {question}")
        print(f"Rewritten Question: {rewritten_question}")
        print("=" * 70)

        # Generate embedding using rewritten question
        query_embedding = (
            self.embedding_service.generate_query_embedding(
                rewritten_question
            )
        )

        # Search Vector DB
        results = self.chroma_service.similarity_search(
            query_embedding=query_embedding,
            top_k=3,
        )

        documents = results.get(
            "documents",
            [[]]
        )[0]

        context = "\n\n".join(documents)

        # Generate final answer using original question
        answer = self.groq_service.generate_answer(
            question=question,
            context=context,
            conversation_history=conversation_history,
        )

        # Store user message
        self.memory_service.add_message(
            session_id=session_id,
            role="user",
            content=question,
        )

        # Store assistant message
        self.memory_service.add_message(
            session_id=session_id,
            role="assistant",
            content=answer,
        )

        return {
            "question": question,
            "rewritten_question": rewritten_question,
            "answer": answer,
            "sources": results.get(
                "metadatas",
                [[]]
            )[0],
        }