from groq import Groq

from app.config.settings import settings


class GroqService:

    def __init__(self):
        self.client = None
        if settings.GROQ_API_KEY:
            self.client = Groq(api_key=settings.GROQ_API_KEY)

    def chat(self, prompt: str):
        if not self.client:
            raise ValueError(
                "GROQ_API_KEY is not configured. Set it in the environment or .env before using GroqService."
            )

        response = self.client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content