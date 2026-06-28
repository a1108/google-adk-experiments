import os

from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from mcp import StdioServerParameters


# Google Maps API Key
google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")


print(f"Google Maps API Key loaded: {bool(google_maps_api_key)}")
print(f"API Key Prefix: {google_maps_api_key[:8] if google_maps_api_key else 'Not Found'}")

if not google_maps_api_key:
    raise ValueError(
        "GOOGLE_MAPS_API_KEY environment variable is not configured."
    )


root_agent = Agent(
    name="google_maps_mcp_agent",
    model="gemini-2.5-flash",
    description=(
        "An AI assistant that uses Google Maps through the "
        "Model Context Protocol (MCP) to answer questions about "
        "locations, routes, directions, nearby places, and place details."
    ),
    instruction="""
You are a Google Maps specialist.

Responsibilities:
- Always use the Google Maps MCP tools for map-related requests.
- Provide accurate directions, routes, travel distance, travel duration,
  nearby places, and place details.
- Do not rely on your own knowledge when Google Maps tools can provide
  real-time information.
- If a user asks a question unrelated to maps, locations, or navigation,
  politely explain that this experiment is focused on Google Maps
  capabilities through MCP.
""",
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",
                        "@modelcontextprotocol/server-google-maps",
                    ],
                    env={
                        "GOOGLE_MAPS_API_KEY": google_maps_api_key,
                    },
                ),
            ),
        )
    ],
)