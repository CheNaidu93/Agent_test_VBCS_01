import re
from typing import Dict, List, Optional


# DEMO DATA ONLY.
# Replace this list with records retrieved from Oracle Fusion REST API later.
SAMPLE_TICKETS = [
    {
        "sr_number": "SR-10025",
        "title": "Unable to submit purchase order",
        "status": "Open",
        "severity": "High",
        "customer": "ABC Technologies",
        "assigned_to": "Venkata Krishna",
        "created_date": "2026-10-20",
        "description": "Purchase order submission fails during validation.",
    },
    {
        "sr_number": "SR-10026",
        "title": "Invoice page loading slowly",
        "status": "Open",
        "severity": "Medium",
        "customer": "Global Systems",
        "assigned_to": "Anita Rao",
        "created_date": "2026-10-19",
        "description": "Invoice search takes longer than expected.",
    },
    {
        "sr_number": "SR-10027",
        "title": "Cannot access supplier portal",
        "status": "Pending",
        "severity": "High",
        "customer": "ABC Technologies",
        "assigned_to": "Rahul Kumar",
        "created_date": "2026-10-18",
        "description": "Supplier portal access needs investigation.",
    },
    {
        "sr_number": "SR-10028",
        "title": "Report output is missing",
        "status": "Closed",
        "severity": "Low",
        "customer": "Northwind Services",
        "assigned_to": "Anita Rao",
        "created_date": "2026-10-15",
        "description": "The requested report output was not generated.",
    },
    {
        "sr_number": "SR-10029",
        "title": "Approval notification not received",
        "status": "Open",
        "severity": "High",
        "customer": "Global Systems",
        "assigned_to": "Venkata Krishna",
        "created_date": "2026-10-21",
        "description": "Approval notification was not received by the requester.",
    },
]


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
            "text": user_message,
        })

        page_type = (
            context.get("page_type", "GENERAL") if context else "GENERAL"
        ).upper()

        record_id = context.get("record_id") if context else None

        if page_type != "SERVICE_REQUEST":
            reply = (
                "Please open this assistant using the SR Bot button "
                "on the Fusion Service Requests page. This assistant "
                "is designed for Service Request tickets."
            )
        else:
            reply = self._route_message(user_message, record_id)

        self.sessions[user_id].append({
            "role": "bot",
            "text": reply,
        })

        return reply

    def _route_message(
        self,
        text: str,
        record_id: Optional[str] = None,
    ) -> str:
        clean = text.lower().strip()

        if clean in {"hi", "hello", "hey", "good morning", "good afternoon"}:
            return (
                "Hello! I am the Service Request (SR) assistant. "
                "Ask me about a specific SR number, all tickets, "
                "or open tickets."
            )

        # Keep customer-profile questions out of the SR assistant.
        customer_terms = (
            "customer profile",
            "customer details",
            "customer account",
            "customer contact",
            "customer context",
            "customer chatbot",
        )
        if any(term in clean for term in customer_terms):
            return (
                "This is the Service Request (SR) chatbot. "
                "I can help with ticket details, ticket status, "
                "severity, assignment, and ticket lists. "
                "Please use the Customer chatbot for customer-profile queries."
            )

        # A ticket number takes priority over a request to list tickets.
        match = re.search(r"\bSR[-\s]?(\d+)\b", text, re.IGNORECASE)

        if match:
            requested_number = f"SR-{match.group(1)}"
            ticket = next(
                (
                    item for item in SAMPLE_TICKETS
                    if item["sr_number"].upper() == requested_number.upper()
                ),
                None,
            )

            if not ticket:
                return (
                    f"I could not find {requested_number} in the current "
                    "ticket data. Please verify the SR number."
                )

            return self._format_ticket(ticket)

        # If the page supplied a specific record ID, use it for a
        # request that refers to "this ticket" or "this SR".
        if record_id and any(
            phrase in clean
            for phrase in ("this ticket", "this sr", "current ticket")
        ):
            normalized_id = record_id.upper().replace(" ", "-")
            ticket = next(
                (
                    item for item in SAMPLE_TICKETS
                    if item["sr_number"].upper() == normalized_id
                ),
                None,
            )
            if ticket:
                return self._format_ticket(ticket)

        # List requests: filter only when the user explicitly asks for open SRs.
        list_terms = (
            "all tickets",
            "all sr",
            "list tickets",
            "list sr",
            "show tickets",
            "show sr",
            "ticket list",
            "ticket summary",
            "how many tickets",
            "number of tickets",
        )

        if any(term in clean for term in list_terms):
            tickets = SAMPLE_TICKETS

            if "open" in clean:
                tickets = [
                    ticket for ticket in tickets
                    if ticket["status"].lower() == "open"
                ]

            return self._format_ticket_list(tickets)

        return (
            "I am the Service Request chatbot. You can ask, for example:\n"
            "• Show SR-10025\n"
            "• List all tickets\n"
            "• Show the ticket summary"
        )

    @staticmethod
    def _format_ticket(ticket: dict) -> str:
        return (
            f"Service Request: {ticket['sr_number']}\n"
            f"Title: {ticket['title']}\n"
            f"Status: {ticket['status']}\n"
            f"Severity: {ticket['severity']}\n"
            f"Customer: {ticket['customer']}\n"
            f"Assigned To: {ticket['assigned_to']}\n"
            f"Created Date: {ticket['created_date']}\n"
            f"Description: {ticket['description']}"
        )

    @staticmethod
    def _format_ticket_list(tickets: List[dict]) -> str:
        if not tickets:
            return "No tickets matched your request."

        lines = [
            f"Service Request Summary — {len(tickets)} ticket(s)",
            "",
            "SR Number | Status | Severity | Assigned To | Title",
            "-" * 75,
        ]

        for ticket in tickets:
            lines.append(
                f"{ticket['sr_number']} | "
                f"{ticket['status']} | "
                f"{ticket['severity']} | "
                f"{ticket['assigned_to']} | "
                f"{ticket['title']}"
            )

        return "\n".join(lines)

    def get_history(self, user_id: str) -> List[Dict[str, str]]:
        return self.sessions.get(user_id, [])


bot_instance = SimpleChatbot()
