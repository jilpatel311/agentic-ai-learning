from groq import Groq

from app.config.settings import settings


class GroqService:

    def __init__(self):
        self.client = None

        if settings.GROQ_API_KEY:
            self.client = Groq(
                api_key=settings.GROQ_API_KEY
            )

        self.model = settings.GROQ_MODEL

    def chat(
        self,
        prompt: str,
    ) -> str:

        if not self.client:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
        )

        return response.choices[0].message.content

    def rewrite_question(
        self,
        question: str,
        conversation_history: list[dict],
    ) -> str:

        if not self.client:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        messages = [
            {
                "role": "system",
                "content": (
                    "You rewrite follow-up questions into standalone questions.\n"
                    "Use the conversation history to resolve references like "
                    "'it', 'that', 'they', 'them', 'this'.\n"
                    "Return ONLY the rewritten question.\n"
                    "If the question is already standalone, return it unchanged."
                )
            }
        ]

        messages.extend(conversation_history)

        messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
        )

        return response.choices[0].message.content.strip()

    def generate_answer(
        self,
        question: str,
        context: str,
        conversation_history: list[dict],
    ) -> str:

        if not self.client:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI Knowledge Assistant.\n"
                    "Answer ONLY using the provided document context.\n"
                    "Use conversation history when required.\n"
                    "If the answer is not available in the provided context, "
                    "reply with 'I couldn't find this information in the uploaded documents.'"
                )
            }
        ]

        messages.extend(conversation_history)

        messages.append(
            {
                "role": "user",
                "content": f"""
Document Context:
--------------------
{context}
--------------------

Question:
{question}
"""
            }
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
        )

        return response.choices[0].message.content