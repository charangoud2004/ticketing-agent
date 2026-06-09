from langchain_groq import ChatGroq
from agent.state import TicketState
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile")

def classify_node(state: TicketState) -> TicketState:
    ticket = state["current_ticket"]
    description = ticket["description"]
    
    prompt = f"""You are a support ticket classifier.
Based on the ticket description below, respond with exactly one word indicating urgency.
Choose only from: low, medium, high, critical

Ticket: {description}

Urgency:"""
    
    response = llm.invoke(prompt)
    urgency = response.content.strip().lower()
    
    if urgency not in ["low", "medium", "high", "critical"]:
        urgency = "medium"
    
    return {"urgency": urgency}


def billing_node(state: TicketState) -> TicketState:
    ticket = state["current_ticket"]
    resolution = {
        "ticket_id": ticket["id"],
        "category": ticket["category"],
        "urgency": state["urgency"],
        "handler_type": "billing",
        "status": "resolved",
        "resolved_at": datetime.now(timezone.utc).isoformat()
    }
    return {"resolutions": state["resolutions"] + [resolution]}


def tech_node(state: TicketState) -> TicketState:
    ticket = state["current_ticket"]
    resolution = {
        "ticket_id": ticket["id"],
        "category": ticket["category"],
        "urgency": state["urgency"],
        "handler_type": "tech",
        "status": "resolved",
        "resolved_at": datetime.now(timezone.utc).isoformat()
    }
    return {"resolutions": state["resolutions"] + [resolution]}


def general_node(state: TicketState) -> TicketState:
    ticket = state["current_ticket"]
    resolution = {
        "ticket_id": ticket["id"],
        "category": ticket["category"],
        "urgency": state["urgency"],
        "handler_type": "general",
        "status": "resolved",
        "resolved_at": datetime.now(timezone.utc).isoformat()
    }
    return {"resolutions": state["resolutions"] + [resolution]}


def escalation_node(state: TicketState) -> TicketState:
    ticket = state["current_ticket"]
    resolution = {
        "ticket_id": ticket["id"],
        "category": ticket["category"],
        "urgency": state["urgency"],
        "handler_type": "escalation",
        "status": "resolved",
        "resolved_at": datetime.now(timezone.utc).isoformat()
    }
    return {"resolutions": state["resolutions"] + [resolution]}


def log_node(state: TicketState) -> TicketState:
    ticket = state["current_ticket"]
    resolution = {
        "ticket_id": ticket["id"],
        "category": ticket["category"],
        "urgency": state["urgency"],
        "handler_type": state["handler_type"],
        "status": "resolved",
        "resolved_at": datetime.now(timezone.utc).isoformat()
    }
    return {"resolutions": state["resolutions"] + [resolution]}