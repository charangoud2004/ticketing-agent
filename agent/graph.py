from langgraph.graph import StateGraph, END
from agent.state import TicketState
from agent.nodes import (
    classify_node,
    billing_node,
    tech_node,
    general_node,
    escalation_node
)

def route_ticket(state: TicketState) -> str:
    urgency = state["urgency"]
    category = state["current_ticket"]["category"].lower()

    if urgency == "critical":
        return "escalation_node"
    elif category == "billing":
        return "billing_node"
    elif category == "tech":
        return "tech_node"
    else:
        return "general_node"


def build_graph():
    graph = StateGraph(TicketState)

    graph.add_node("classify_node", classify_node)
    graph.add_node("billing_node", billing_node)
    graph.add_node("tech_node", tech_node)
    graph.add_node("general_node", general_node)
    graph.add_node("escalation_node", escalation_node)

    graph.set_entry_point("classify_node")

    graph.add_conditional_edges(
        "classify_node",
        route_ticket,
        {
            "billing_node": "billing_node",
            "tech_node": "tech_node",
            "general_node": "general_node",
            "escalation_node": "escalation_node"
        }
    )

    graph.add_edge("billing_node", END)
    graph.add_edge("tech_node", END)
    graph.add_edge("general_node", END)
    graph.add_edge("escalation_node", END)

    return graph.compile()