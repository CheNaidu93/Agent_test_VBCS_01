from typing import Dict, List

class SimpleChatbot:
    def __init__(self):
        self.sessions: Dict[str, List[Dict[str, str]]] = {}

    def get_response(self, user_id: str, user_message: str) -> str:
        if user_id not in self.sessions:
            self.sessions[user_id] = []

        self.sessions[user_id].append({"role": "user", "text": user_message})

        # Generate response (rule-based or LLM connection)
        bot_reply = self._rule_engine(user_message)

        self.sessions[user_id].append({"role": "bot", "text": bot_reply})
        return bot_reply

    def _rule_engine(self, text: str) -> str:
        clean = text.lower().strip()
        if "hello" in clean or "hi" in clean:
            return "Greetings! How can I help you today?"
        elif "services" in clean:
            return "We provide automated support, REST integration, and intelligent chat features."
        return f"Received message: '{text}'."

    def get_history(self, user_id: str) -> List[Dict[str, str]]:
        return self.sessions.get(user_id, [])

bot_instance = SimpleChatbot()
