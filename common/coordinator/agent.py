from google.adk.agents import Agent
from google.adk.tools import AgentTool
from context_agent import root_agent as context_agent
from mcp_integration import root_agent as maps_agent


root_agent = Agent(
    name="coordinator_agent",
    model="gemini-2.5-flash",
    description=(
        "Coordinator agent responsible for routing user requests "
        "to the appropriate specialist agent."
    ),
    instruction="""
You are the coordinator of a multi-agent system.

Your job is to determine which specialist agent should handle the user's request.

Routing Rules:

1. Delegate to the Google Maps MCP Agent for:
   - maps
   - directions
   - navigation
   - travel routes
   - travel distance
   - travel duration
   - nearby places
   - restaurants
   - hotels
   - landmarks
   - addresses
   - locations

2. Delegate to the Conversation Context Agent for:
   - general conversation
   - programming
   - explanations
   - follow-up questions
   - any topic unrelated to maps

Never answer directly.

You have two tools:

1. conversation_context_agent
2. google_maps_mcp_agent

For every request, call exactly one of these tools.

After the tool returns, return its answer to the user without modification.
""",
    tools=[
            AgentTool(context_agent),
            AgentTool(maps_agent)
            ],
)