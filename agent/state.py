from typing import TypedDict, List

class TicketState(TypedDict):
    current_ticket: dict
    urgency: str
    handler_type: str
    resolutions: List[dict]