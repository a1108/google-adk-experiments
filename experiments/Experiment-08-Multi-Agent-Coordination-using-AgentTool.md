# Experiment 08 - Multi-Agent Coordination using AgentTool

## bjective

Understand how a Coordinator Agent delegates user requests to specialist agents using AgentTool in Google ADK.

This experiment verifies how Google ADK performs semantic routing, invokes specialist agents, and returns responses through a coordinator.

⸻

## Research Question

* What is a Coordinator Agent?
* How does semantic routing work?
* How does AgentTool delegate requests?
* What is an Invocation?
* How does the execution flow appear in ADK Trace?

⸻

## Experiment Setup

Item	Value
Framework	Google ADK
Model	Gemini 2.5 Flash
Architecture	Multi-Agent
Coordinator	Coordinator Agent
Specialist Agents	Conversation Context Agent, Google Maps MCP Agent
Delegation Mechanism	AgentTool
Verification	Runtime + ADK Trace

⸻

## Architecture

```text
                    User
                      │
                      ▼
              Coordinator Agent
                      │
          Semantic Routing (LLM)
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
Conversation Context Agent    Google Maps MCP Agent
        │                           │
        ▼                           ▼
 Generate Answer           Execute Maps MCP Tools
        │                           │
        └─────────────┬─────────────┘
                      ▼
             Coordinator Agent
                      │
                      ▼
                     User
```

⸻

## Components

Component	Responsibility
Coordinator Agent	Determines which specialist agent should handle the request
Conversation Context Agent	Answers general conversation and programming questions
Google Maps MCP Agent	Handles maps, navigation, directions, nearby places, and travel queries
Gemini 2.5 Flash	Performs semantic routing and generates responses
AgentTool	Executes specialist agents as tools

⸻

## Routing Rules

Conversation Context Agent

Handles requests related to:

* Programming
* Java
* Spring Boot
* General knowledge
* Follow-up questions
* Conversation context

⸻

Google Maps MCP Agent

Handles requests related to:

* Maps
* Directions
* Navigation
* Nearby places
* Restaurants
* Hotels
* Landmarks
* Travel routes
* Addresses

⸻

## Runtime Flow

```text
User
   │
   ▼
Coordinator Agent
   │
   ├── call_llm
   │
   ├── generate_content (Gemini 2.5 Flash)
   │        │
   │        ▼
   │  Gemini decides which specialist
   │  agent should handle the request.
   │
   ├── execute_tool
   │        │
   │        ▼
   │  Invocation starts
   │
   ▼
Specialist Agent
   │
   ├── call_llm
   │
   ├── generate_content
   │
   ▼
Returns answer
   │
   ▼
Coordinator Agent
   │
   ▼
User
```
⸻

## Understanding Invocation

An Invocation represents the execution of a specialist agent after it has been selected by the Coordinator Agent.

Execution lifecycle:

```text
Coordinator Agent
        │
        ▼
execute_tool()
        │
        ▼
Invocation Created
        │
        ▼
Specialist Agent Executes
        │
        ▼
Returns Result
        │
        ▼
Invocation Ends
        │
        ▼
Coordinator Continues Execution

```

Invocation is not a new conversation.

It simply represents the runtime execution context of the delegated agent.

⸻

## Runtime Verification

Example Request

Tell me about Java 8.

Observed execution:

1. User sends the request.
2. Coordinator Agent calls Gemini.
3. Gemini semantically classifies the request.
4. Gemini selects the Conversation Context Agent.
5. ADK executes the agent using AgentTool.
6. An Invocation is created.
7. Conversation Context Agent generates the answer.
8. Result is returned to the Coordinator.
9. Coordinator returns the final response to the user.

⸻

## Semantic Routing

Unlike traditional rule-based routing, the Coordinator does not manually inspect keywords.

Instead, Gemini understands the user’s intent and determines which specialist agent is most appropriate.

Examples:

User Request	Routed To
Tell me about Java 8	Conversation Context Agent
Explain Spring Boot	Conversation Context Agent
Directions from Delhi to Agra	Google Maps MCP Agent
Find nearby restaurants	Google Maps MCP Agent

⸻

## Key Concepts

Concept	Description
Coordinator Agent	Entry point for all user requests
Semantic Routing	LLM determines the best specialist agent
AgentTool	Executes another agent as a tool
Invocation	Runtime execution of the delegated agent
Specialist Agent	Generates the actual response

⸻

## Findings

* ✅ Coordinator Agent does not directly answer specialist questions.
* ✅ Gemini performs semantic routing based on user intent.
* ✅ AgentTool delegates execution to specialist agents.
* ✅ Each delegated agent executes inside its own Invocation.
* ✅ Specialist agents have their own prompts and LLM calls.
* ✅ The Coordinator receives the specialist response and returns it to the user.

⸻

## Key Takeaways

* Coordinator Agent acts as the orchestrator.
* Gemini performs intelligent semantic routing.
* AgentTool enables one agent to execute another agent.
* Invocation represents the runtime execution of a delegated agent.
* Specialist agents remain independent and reusable.
* This architecture scales naturally as additional specialist agents are introduced.

⸻

## Verification Checklist

* ✅ Documentation Verified
* ✅ Runtime Verified
* ✅ ADK Trace Verified
* ✅ AgentTool Verified
* ✅ Invocation Verified

⸻

## Conclusion

This experiment confirmed how Google ADK implements a multi-agent architecture using AgentTool.

Instead of hardcoded routing logic, the Coordinator Agent relies on Gemini’s semantic understanding to determine the most appropriate specialist agent. Google ADK then creates an Invocation to execute the selected agent, returns the generated response to the Coordinator, and finally delivers the response to the user.

This orchestration model provides a clean, modular, and extensible approach for building scalable multi-agent systems.