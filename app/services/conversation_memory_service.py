class ConversationMemoryService:

    def __init__(self):
        self.sessions: dict[str, list[dict]] = {}

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ):

        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append(
            {
                "role": role,
                "content": content,
            }
        )

    def get_messages(
        self,
        session_id: str,
    ) -> list[dict]:

        return self.sessions.get(session_id, [])

    def clear_session(
        self,
        session_id: str,
    ):

        self.sessions.pop(session_id, None)