import json

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
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
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
                ),
            }
        ]

        messages.extend(
            conversation_history
        )

        messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=messages,
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
                ),
            }
        ]

        messages.extend(
            conversation_history
        )

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
""",
            }
        )

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=messages,
        )

        return response.choices[0].message.content

    def detect_tool(
        self,
        question: str,
    ) -> str:

        if not self.client:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": """
You are an AI routing assistant.

Available tools:

calculator
database
rag

Return ONLY one word.

calculator
database
rag
""",
                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
        )

        tool = (
            response.choices[0]
            .message.content
            .strip()
            .lower()
        )

        if tool not in (
            "calculator",
            "database",
            "rag",
        ):
            return "rag"

        return tool

    def create_execution_plan(
        self,
        question: str,
    ) -> dict:

        if not self.client:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": """
You are an AI Agent Planner.

Your job is to decide which tool should be used.

You have three tools:

1. calculator
Use for:
- mathematical calculations
- arithmetic
- percentages
- multiplication
- division
- addition
- subtraction

Examples:
User: Calculate 25 * 10
Output:
{
    "tool":"calculator",
    "expression":"25*10"
}

------------------------------------------------

2. database

Use for employee-related questions.

Examples:

User: How many employees are there?

Output:
{
    "tool":"database",
    "action":"employee_count"
}

User: What is Rahul Sharma salary?

Output:
{
    "tool":"database",
    "action":"employee_salary",
    "employee_name":"Rahul Sharma"
}

User: How many reward points Rahul Sharma have?

Output:
{
    "tool":"database",
    "action":"employee_reward_points",
    "employee_name":"Rahul Sharma"
}

User: What is Rahul Sharma leave balance?

Output:
{
    "tool":"database",
    "action":"employee_leave_balance",
    "employee_name":"Rahul Sharma"
}

User: Show Engineering employees

Output:
{
    "tool":"database",
    "action":"employees_by_department",
    "department":"Engineering"
}

User: In which department Rahul Sharma is working?
Output:
{
    "tool":"database",
    "action":"employee_department",
    "employee_name":"Rahul Sharma"
}

User: Who has the highest salary?

Output:
{
    "tool":"database",
    "action":"highest_salary"
}

------------------------------------------------

3. rag

Use for:

- PDF
- Uploaded documents
- Leave policy
- HR policy
- Company policy
- Knowledge base

Examples:

User: What is leave encashment?

Output:
{
    "tool":"rag"
}

User: How many casual leaves employees have?

Output:
{
    "tool":"rag"
}

------------------------------------------------

IMPORTANT:

Return ONLY valid JSON.

Do not explain.

Do not use markdown.

Return only the JSON object.
""",
                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
        )

        try:

            return json.loads(
                response.choices[0].message.content
            )

        except Exception:

            return {
                "tool": "rag"
            }

    def generate_tool_response(
        self,
        question: str,
        tool_name: str,
        tool_result,
    ) -> str:

        if not self.client:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI Assistant.\n"
                        "Answer the user's question naturally using ONLY the provided tool result.\n"
                        "Do not make up information.\n"
                        "If the tool result is empty or null, clearly state that no information was found."
                    ),
                },
                {
                    "role": "user",
                    "content": f"""
Question:
{question}

Tool Used:
{tool_name}

Tool Result:
{json.dumps(tool_result, indent=2)}
""",
                },
            ],
        )

        return response.choices[0].message.content