# Ticketing Agent - LangGraph Ticket Triage System

An automated support ticket triage system built with LangGraph that classifies tickets by urgency using an LLM and routes them to appropriate handlers.

## Features

- **Automated Classification**: Uses Groq LLM to analyze ticket descriptions and assign urgency levels (low, medium, high, critical)
- **Smart Routing**: Routes tickets to specialized handlers based on urgency and category
- **Handler Simulation**: Simulates resolution through billing, tech, general, and escalation handlers
- **Structured Logging**: Outputs comprehensive resolution logs in JSON format

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/charangoud2004/ticketing-agent.git
   cd ticketing-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   Then add your `GROQ_API_KEY` to the `.env` file

4. **Run the agent**
   ```bash
   python main.py
   ```

## How It Works

```
data/tickets.json 
    ↓
Classify (Groq LLM)
    ↓
Route by urgency + category
    ↓
Handler (billing/tech/general/escalation)
    ↓
data/resolution_log.json
```

### Workflow Details

1. **Ingestion**: Reads support tickets from `data/tickets.json`
2. **Classification**: LLM analyzes ticket description and assigns urgency level
3. **Routing Logic**:
   - **Critical urgency** → Escalation Handler (regardless of category)
   - **Billing category** → Billing Handler
   - **Tech category** → Tech Handler
   - **General category** → General Handler
4. **Resolution**: Each handler creates a resolution record with status and timestamp
5. **Output**: All resolutions written to `data/resolution_log.json`

## Project Structure

```
ticketing-agent/
├── agent/
│   ├── state.py        # TypedDict state definition
│   ├── nodes.py        # LLM classifier and handler nodes
│   └── graph.py        # LangGraph workflow definition
├── data/
│   ├── tickets.json    # Input tickets
│   └── resolution_log.json  # Output resolutions
├── main.py             # Entry point
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
└── README.md
```

## Input Format

Tickets in `data/tickets.json`:
```json
[
  {
    "id": "TKT-001",
    "description": "Payment processing is down...",
    "category": "billing",
    "submitted_at": "2026-06-09T14:23:00Z"
  }
]
```

## Output Format

Resolutions in `data/resolution_log.json`:
```json
[
  {
    "ticket_id": "TKT-001",
    "urgency": "critical",
    "category": "billing",
    "handler_type": "escalation",
    "status": "resolved",
    "resolved_at": "2026-06-09T14:23:45.123Z"
  }
]
```

## AI Usage Documentation

This project was built with AI assistance as part of a learning exercise:

### Kiro Spec Mode
- Used **Kiro's Spec-driven workflow** to generate a comprehensive requirements document
- Created structured requirements with user stories, acceptance criteria, and EARS format
- Established clear specifications for LLM integration, state management, and error handling

### Claude AI Assistance
- Used **Claude** to understand LangGraph concepts and architecture patterns
- Learned StateGraph design, node creation, and conditional routing
- Received guidance on LangChain integration with Groq API

### Implementation Approach
- Code written **manually** with AI assistance for learning and understanding
- AI used primarily for:
  - Architecture guidance and best practices
  - Debugging and error resolution
  - Documentation and code structure suggestions
- Hands-on coding to ensure deep understanding of LangGraph workflow mechanics

## Technologies

- **LangGraph**: State graph workflow orchestration
- **LangChain**: LLM integration framework
- **Groq API**: Fast LLM inference (llama-3.3-70b-versatile)
- **Python**: Core implementation language

## Requirements

- Python 3.8+
- Groq API key (get one at [console.groq.com](https://console.groq.com))

## License

MIT

## Author

Built by [@charangoud2004](https://github.com/charangoud2004) as part of an enterprise automation challenge.
