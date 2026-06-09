# Requirements Document

## Introduction

The Ticketing Agent is an automated support ticket triage system built with LangGraph. The system ingests support tickets from a JSON file, classifies each ticket by urgency using an LLM, routes tickets to appropriate handlers based on urgency and category, simulates resolution through handler nodes, and outputs structured resolution logs.

## Glossary

Triage_Agent: The LangGraph-based state graph that orchestrates the ticket classification and routing workflow
Ticket: A support request with fields: id, description, category, and submitted_at timestamp
Urgency_Classifier: The LLM-powered component that assigns urgency levels to tickets
Urgency_Level: One of four values: low, medium, high, or critical
Handler: A node in the state graph that simulates resolution for a specific ticket type
Billing_Handler: Handler for billing-related tickets
Tech_Handler: Handler for technical support tickets
General_Handler: Handler for general inquiry tickets
Escalation_Handler: Handler for critical tickets requiring immediate attention
- **Resolution_Log**: JSON output file containing the results of ticket processing

## Requirements

### Requirement 1: Ticket Ingestion

**User Story:** As a support operations manager, I want the system to ingest tickets from a JSON file, so that existing ticket data can be processed automatically.

#### Acceptance Criteria

WHEN the Triage_Agent starts, THE Triage_Agent SHALL read all tickets from data/tickets.json
THE Triage_Agent SHALL parse data/tickets.json as a JSON array where each element represents a ticket
THE Triage_Agent SHALL parse each ticket into a structured object with id, description, category, and submitted_at fields
THE Triage_Agent SHALL validate that each required field (id, description, category, submitted_at) is present and non-empty
IF data/tickets.json does not exist or cannot be read, THEN THE Triage_Agent SHALL log a clear error message and terminate execution
IF data/tickets.json contains invalid JSON or is not a JSON array, THEN THE Triage_Agent SHALL log an error and terminate execution
IF data/tickets.json contains an empty array, THEN THE Triage_Agent SHALL log a warning and terminate execution
- IF a ticket is missing required fields, THEN THE Triage_Agent SHALL log a validation error for that ticket and continue processing the remaining tickets


### Requirement 2: Urgency Classification

**User Story:** As a support team lead, I want tickets automatically classified by urgency, so that critical issues receive immediate attention.

#### Acceptance Criteria

FOR ALL valid tickets, THE Urgency_Classifier SHALL assign an Urgency_Level using the Groq LLM API
THE Urgency_Classifier SHALL analyze the ticket description to determine urgency
THE Urgency_Classifier SHALL output exactly one Urgency_Level per ticket: low, medium, high, or critical
IF the LLM API call fails or returns an unrecognized value, THEN THE Urgency_Classifier SHALL assign a default Urgency_Level of medium and log the failure with the ticket id
- IF a ticket description is empty, THEN THE Urgency_Classifier SHALL assign a default Urgency_Level of medium and log a warning


### Requirement 3: Ticket Routing

**User Story:** As a support coordinator, I want tickets routed to specialized handlers, so that each ticket reaches the appropriate resolution team.

#### Acceptance Criteria

WHEN a ticket has Urgency_Level of critical, THE Triage_Agent SHALL route it to the Escalation_Handler regardless of category
IF urgency is low, medium, or high AND category is billing → route to Billing_Handler
IF urgency is low, medium, or high AND category is tech → route to Tech_Handler
IF urgency is low, medium, or high AND category is general → route to General_Handler
THE Triage_Agent SHALL perform case-insensitive matching on category values
IF a ticket has an unrecognized category, THE Triage_Agent SHALL route it to the General_Handler and log a warning
- Each ticket SHALL be routed to exactly one handler


### Requirement 4: Ticket Resolution Simulation

**User Story:** As a system developer, I want handlers to simulate ticket resolution so the workflow can be tested end-to-end.

#### Acceptance Criteria

Each handler (Billing, Tech, General, Escalation) SHALL create a resolution record with its corresponding handler_type
- Each resolution record SHALL include: ticket_id, category, urgency, handler_type, status (set to "resolved"), and resolved_at timestamp in ISO 8601 format


### Requirement 5: Resolution Log Output

**User Story:** As a support operations manager, I want all resolutions logged to a JSON file so I can audit ticket processing results.

#### Acceptance Criteria

WHEN all tickets are processed, THE Triage_Agent SHALL write all resolution records to data/resolution_log.json
Output SHALL be a valid JSON array with 2-space indentation
Each record SHALL include: ticket_id, urgency, category, handler_type, status, resolved_at
IF data/resolution_log.json already exists, THE Triage_Agent SHALL overwrite it
IF the data directory does not exist, THE Triage_Agent SHALL create it before writing
- IF writing fails, THE Triage_Agent SHALL log the error and terminate


### Requirement 6: LangGraph State Management

**User Story:** As a system developer, I want typed state management in LangGraph so the workflow maintains data integrity throughout execution.

#### Acceptance Criteria

THE Triage_Agent SHALL define a StateGraph with typed state (TypedDict) containing: current_ticket, urgency, category, handler_type, and resolutions list
THE Triage_Agent SHALL maintain current ticket data in state while processing
THE Triage_Agent SHALL accumulate all resolution records in the state resolutions list
THE Triage_Agent SHALL transition state through nodes: ingestion → classification → routing → handler → output
- WHEN an error occurs during state transitions, THE Triage_Agent SHALL log the error with the current node name and error details


### Requirement 7: LLM API Integration

**User Story:** As a system administrator, I want the system to use Groq for LLM calls via LangChain's ChatGroq integration.

#### Acceptance Criteria

THE Urgency_Classifier SHALL use Groq API via LangChain's ChatGroq client
THE Urgency_Classifier SHALL read the Groq API key from the GROQ_API_KEY environment variable
IF no API key is found, THE Triage_Agent SHALL log an error and terminate before processing tickets
- THE Urgency_Classifier SHALL include the ticket description in the LLM prompt and parse the response to extract the Urgency_Level


### Requirement 8: Error Handling and Logging

**User Story:** As a system operator, I want comprehensive error logging so I can diagnose issues quickly.

#### Acceptance Criteria

WHEN an error occurs in any component, THE Triage_Agent SHALL log the error with timestamp, component name, and error details
THE Triage_Agent SHALL continue processing remaining tickets after non-critical errors
IF a critical error occurs during initialization, THE Triage_Agent SHALL terminate with a non-zero exit code
THE Triage_Agent SHALL log the start and completion of each processing phase
WHEN processing completes, THE Triage_Agent SHALL log a summary with total tickets processed and resolution counts by handler type