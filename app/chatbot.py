
from typing import Dict, List, Optional


class SimpleChatbot:
    def __init__(self):
        self.sessions: Dict[str, List[Dict[str, str]]] = {}

    def get_response(
        self,
        user_id: str,
        user_message: str,
        context: Optional[dict] = None,
    ) -> str:
        if user_id not in self.sessions:
            self.sessions[user_id] = []

        self.sessions[user_id].append({
            "role": "user",
            "text": user_message
        })

        page_type = (
            context.get("page_type", "GENERAL")
            if context else "GENERAL"
        ).upper()

        record_id = (
            context.get("record_id")
            if context else None
        )

        bot_reply = self._route_message(
            user_message,
            page_type,
            record_id
        )

        self.sessions[user_id].append({
            "role": "bot",
            "text": bot_reply
        })

        return bot_reply

    def _route_message(
        self,
        text: str,
        page_type: str,
        record_id: Optional[str],
    ) -> str:
        clean = text.lower().strip()

        # Preserve existing general chatbot behavior.
        if "hello" in clean or clean == "hi":
            return "Greetings! How can I help you today?"

        if "services" in clean:
            return (
                "We provide automated support, REST integration, "
                "and intelligent chat features."
            )

        # Context-aware routing.
        if page_type == "CUSTOMER":
            if not record_id:
                return (
                    "You are on a customer page, but no customer "
                    "identifier was provided."
                )

            return (
                "Customer context detected for record "
                f"{record_id}. The Fusion customer lookup "
                "integration still needs to be configured "
                "to retrieve actual customer details."
            )

        if page_type in ("SERVICE_REQUEST", "SERVICE"):
            if not record_id:
                return (
                    "You are on a service request page, but no "
                    "service request identifier was provided."
                )

            return (
                "Service request context detected for record "
                f"{record_id}. The Fusion service request lookup "
                "integration still needs to be configured "
                "to retrieve actual ticket details."
            )

        return f"Received message: '{text}'."

    def get_history(
        self,
        user_id: str
    ) -> List[Dict[str, str]]:
        return self.sessions.get(user_id, [])


bot_instance = SimpleChatbot()
