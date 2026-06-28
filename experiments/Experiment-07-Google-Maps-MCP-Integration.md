# Experiment 07 - Google Maps MCP Integration

## Objective

Understand how Google ADK integrates with a Model Context Protocol (MCP) server to access Google Maps capabilities.

This experiment verifies how an ADK agent discovers MCP tools, invokes them, processes tool responses, and generates answers using real-time Google Maps data.

---

## Research Questions

- What is Model Context Protocol (MCP)?
- How does Google ADK connect to an MCP server?
- How are MCP tools discovered?
- How does the agent invoke Google Maps tools?
- How does the execution flow appear in the ADK Trace?

---

## Experiment Setup

| Item | Value |
|------|------|
| Framework | Google ADK |
| Model | Gemini 2.5 Flash |
| Integration | Google Maps MCP Server |
| Connection | Stdio |
| Server | @modelcontextprotocol/server-google-maps |
| Tool Provider | MCP |

---

## Architecture

```text
             User
               │
               ▼
        Google Maps Agent
               │
         Gemini 2.5 Flash
               │
     Function Calling Decision
               │
               ▼
        Google ADK MCPToolset
               │
         Stdio Connection
               │
               ▼
Google Maps MCP Server (Node.js)
               │
               ▼
      Google Maps APIs
               │
               ▼
        Tool Response
               │
               ▼
       Google Maps Agent
               │
               ▼
             User
```

---

## Components

| Component | Responsibility |
|------------|----------------|
| Google Maps Agent | Handles map-related requests |
| Gemini 2.5 Flash | Determines which MCP tool to call |
| MCPToolset | Exposes MCP tools to the LLM |
| MCP Server | Executes Google Maps operations |
| Google Maps APIs | Returns live map data |

---

## Available MCP Tools

The following tools are automatically discovered from the Google Maps MCP Server:

- `maps_geocode`
- `maps_reverse_geocode`
- `maps_search_places`
- `maps_place_details`
- `maps_distance_matrix`
- `maps_directions`
- `maps_elevation`

---

## Runtime Flow

```text
User
   │
   ▼
Google Maps Agent
   │
   ▼
call_llm
   │
   ▼
Gemini selects an MCP Tool
   │
   ▼
execute_tool
   │
   ▼
MCP Server
   │
   ▼
Google Maps API
   │
   ▼
Tool Response
   │
   ▼
Google Maps Agent
   │
   ▼
Final Answer
```

---

## Runtime Verification

### Example 1

#### User Request

```text
How far is Delhi from Agra?
```

#### Observed Execution

1. The Google Maps Agent receives the request.
2. Gemini selects `maps_distance_matrix`.
3. ADK invokes the MCP tool.
4. The Google Maps MCP server calls the Distance Matrix API.
5. The API returns a **LegacyApiNotActivated** error.
6. Gemini reasons over the tool failure.
7. Gemini invokes `maps_directions`.
8. The Directions API returns the route information.
9. The agent summarizes the distance and travel duration.
10. The final response is returned to the user.

---

### Example 2

#### User Request

```text
Distance between Delhi Station and Noida Microsoft Office
```

#### Observed Execution

1. Gemini selects `maps_distance_matrix`.
2. The Distance Matrix API returns an error.
3. Gemini automatically invokes `maps_directions`.
4. The Directions API returns:

   - Distance: **26.6 km**
   - Duration: **43 minutes**

5. The agent generates the final response.

---

## ADK Trace Observation

```text
call_llm
      │
      ▼
function_call
(maps_distance_matrix)
      │
      ▼
execute_tool
      │
      ▼
Tool Error
(LegacyApiNotActivated)
      │
      ▼
call_llm
      │
      ▼
function_call
(maps_directions)
      │
      ▼
execute_tool
      │
      ▼
Tool Success
      │
      ▼
Final Answer
```

The trace demonstrates that Gemini can perform **multi-step tool reasoning**, selecting an alternative tool when the initial tool invocation fails.

---

## Error Handling

During testing, the `maps_distance_matrix` tool returned the following error:

```text
LegacyApiNotActivatedMapError
```

### Reason

- The Google Maps MCP server invokes the legacy Distance Matrix API.
- The legacy API was not enabled for the configured Google Cloud project.

Instead of terminating, Gemini automatically selected the `maps_directions` tool, which successfully returned the required travel information.

This demonstrates **LLM-driven tool recovery**, where the model reasons over tool failures and selects an alternative tool to complete the task.

---

## Key Concepts

| Concept | Description |
|----------|-------------|
| MCP | Standard protocol for exposing external tools to LLMs |
| MCPToolset | Registers MCP tools with the agent |
| Stdio Connection | Communication channel between ADK and the MCP server |
| Function Calling | Gemini determines which tool should be invoked |
| Tool Execution | MCP server executes the requested operation |
| Tool Recovery | Gemini invokes an alternative tool when the first tool fails |

---

## Findings

- ✅ Google ADK successfully connected to the Google Maps MCP Server.
- ✅ MCP tools were automatically discovered.
- ✅ Gemini selected tools based on user intent.
- ✅ ADK executed MCP tools through the `MCPToolset`.
- ✅ Tool responses were incorporated into the final answer.
- ✅ Gemini demonstrated adaptive reasoning by recovering from a failed tool invocation using an alternative Maps tool.

---

## Key Takeaways

- Google ADK integrates external capabilities through the Model Context Protocol (MCP).
- MCPToolset automatically exposes server capabilities as callable tools.
- Gemini determines which MCP tool to invoke using function calling.
- ADK manages communication with the MCP server over a Stdio connection.
- Gemini can recover from tool failures by selecting another appropriate tool.
- MCP enables agents to use real-time Google Maps functionality without implementing custom API integrations.

---

## Verification Checklist

- ✅ Documentation Verified
- ✅ Runtime Verified
- ✅ ADK Trace Verified
- ✅ MCPToolset Verified
- ✅ Function Calling Verified
- ✅ Tool Recovery Verified

---

## Conclusion

This experiment confirmed how Google ADK integrates with external systems using the Model Context Protocol (MCP). The Google Maps Agent successfully discovered tools exposed by the MCP server, invoked them through the `MCPToolset`, and generated responses using live Google Maps data. The experiment also demonstrated Gemini's ability to perform adaptive tool reasoning by recovering from a failed `maps_distance_matrix` invocation through the successful use of `maps_directions`, illustrating the robustness and flexibility of MCP-based tool integration.