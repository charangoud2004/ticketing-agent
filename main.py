import json
import os
from agent.graph import build_graph

def main():
    with open("data/tickets.json", "r") as f:
        tickets = json.load(f)

    graph = build_graph()
    all_resolutions = []

    for ticket in tickets:
        print(f"Processing {ticket['id']}...")
        
        result = graph.invoke({
            "current_ticket": ticket,
            "urgency": "",
            "handler_type": "",
            "resolutions": []
        })
        
        all_resolutions.extend(result["resolutions"])

    os.makedirs("data", exist_ok=True)
    with open("data/resolution_log.json", "w") as f:
        json.dump(all_resolutions, f, indent=2)

    print(f"\nDone. {len(all_resolutions)} tickets resolved.")
    print(json.dumps(all_resolutions, indent=2))

if __name__ == "__main__":
    main()