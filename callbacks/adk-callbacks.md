# Callbacks: Observe, Customize, and Control Agent Behavior

Callbacks are a cornerstone feature of ADK, providing a powerful mechanism to hook into an agent's execution process. They allow you to observe, customize, and even control the agent's behavior at specific, predefined points without modifying the core ADK framework code.

## What are they?

In essence, callbacks are standard functions that you define. You then associate these functions with an agent when you create it. The ADK framework automatically calls your functions at key stages, letting you observe or intervene. Think of it like checkpoints during the agent's process:

- **Before the agent starts its main work on a request, and after it finishes:**
  - The `Before Agent` callback executes *right before* this main work begins for that specific request.
  - The `After Agent` callback executes *right after* the agent has finished all its steps for that request and has prepared the final result, but just before the result is returned.
  - This "main work" encompasses the agent's *entire* process for handling that single request — deciding to call an LLM, actually calling the LLM, deciding to use a tool, using the tool, processing results, and finally putting together the answer.

- **Before sending a request to, or after receiving a response from, the LLM:**
  - `Before Model` and `After Model` callbacks let you inspect or modify the data going to and coming from the LLM specifically.

- **Before executing a tool (like a Python function or another agent) or after it finishes:**
  - `Before Tool` and `After Tool` callbacks give you control points specifically around tool execution.

## Why use them?

- **Observe & Debug:** Log detailed information at critical steps for monitoring and troubleshooting.
- **Customize & Control:** Modify data flowing through the agent (like LLM requests or tool results) or bypass certain steps entirely based on your logic.
- **Implement Guardrails:** Enforce safety rules, validate inputs/outputs, or prevent disallowed operations.
- **Manage State:** Read or dynamically update the agent's session state during execution.
- **Integrate & Enhance:** Trigger external actions (API calls, notifications) or add features like caching.


## How are they added (basic example — Python)

```python
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from typing import Optional

# --- Define your callback function ---
def my_before_model_logic(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    print(f"Callback running before model call for agent: {callback_context.agent_name}")
    # ... your custom logic here ...
    return None  # Allow the model call to proceed

# --- Register it during Agent creation ---
my_agent = LlmAgent(
    name="MyCallbackAgent",
    model="gemini-2.0-flash",  # Or your desired model
    instruction="Be helpful.",
    # Other agent parameters...
    before_model_callback=my_before_model_logic  # Pass the function here
)
```

## The Callback Mechanism: Interception and Control

When the ADK framework encounters a point where a callback can run (e.g., just before calling the LLM), it checks if you provided a corresponding callback function for that agent. If you did, the framework executes your function.

**Context is Key:** Your callback function isn't called in isolation. The framework provides special **context objects** (`CallbackContext` or `ToolContext`) as arguments. These objects contain vital information about the current state of the agent's execution, including invocation details, session state, and potentially references to services like artifacts or memory.

**Controlling the Flow (The Core Mechanism):** The most powerful aspect of callbacks lies in how their **return value** influences the agent's subsequent actions:

### 1. `return None` (Allow Default Behavior)

- The specific return type varies by language: `Optional.empty()` in Java; `CallbackChoice.Continue(value)` (for `before_*` callbacks) or the original object (for `after_*` callbacks) in Kotlin.
- This is the standard way to signal that your callback has finished its work (logging, inspection, minor modifications) and that the ADK agent should **proceed with its normal operation**.
- For `before_*` callbacks (`before_agent`, `before_model`, `before_tool`), returning "Continue" means the next step in the sequence occurs (running agent logic, calling the LLM, executing the tool).
- For `after_*` callbacks (`after_agent`, `after_model`, `after_tool`), returning the result just produced as-is means the framework continues processing.

### 2. `return <Specific Object>` (Override Default Behavior)

Returning a specific object (instead of "Continue") is how you **override** the ADK agent's default behavior. In Kotlin this is `CallbackChoice.Break(value)` for `before_*` callbacks, or a replacement object for `after_*` callbacks. The framework uses the object you return and *skips* the step that would normally follow, or *replaces* the result just generated.

| Callback | Override behavior |
|---|---|
| `before_agent_callback` → `CallbackChoice.Break(Content)` | Skips the agent's main execution logic. The returned `Content` is immediately treated as the agent's final output for this turn. Useful for handling simple requests directly or enforcing access control. |
| `before_model_callback` → `CallbackChoice.Break(LlmResponse)` | Skips the call to the external LLM. The returned `LlmResponse` is processed as if it were the actual LLM response. Ideal for input guardrails, prompt validation, or serving cached responses. |
| `before_tool_callback` → `CallbackChoice.Break(Map<String, Any>)` | Skips execution of the actual tool function (or sub-agent). The returned `Map` is used as the tool call result, typically passed back to the LLM. Perfect for validating tool arguments, applying policy restrictions, or returning mocked/cached results. |
| `after_agent_callback` → `Content` | *Replaces* the `Content` that the agent's run logic just produced. |
| `after_model_callback` → `LlmResponse` | *Replaces* the `LlmResponse` received from the LLM. Useful for sanitizing outputs, adding disclaimers, or modifying response structure. |
| `after_tool_callback` → `Map<String, Any>` | *Replaces* the `Map` result returned by the tool. Allows post-processing or standardization of tool outputs before they go back to the LLM. |

## Conceptual Code Example (Guardrail)

This example demonstrates the common pattern for a guardrail using `before_model_callback` — inspecting the last user message, modifying the system instruction, and blocking the LLM call if the message contains "BLOCK".

### Python

```python
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from google.adk.runners import Runner
from typing import Optional
from google.genai import types
from google.adk.sessions import InMemorySessionService

GEMINI_2_FLASH = "gemini-2.0-flash"

# --- Define the Callback Function ---
def simple_before_model_modifier(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Inspects/modifies the LLM request or skips the call."""
    agent_name = callback_context.agent_name
    print(f"[Callback] Before model call for agent: {agent_name}")

    # Inspect the last user message in the request contents
    last_user_message = ""
    if llm_request.contents and llm_request.contents[-1].role == 'user':
        if llm_request.contents[-1].parts:
            last_user_message = llm_request.contents[-1].parts[0].text
    print(f"[Callback] Inspecting last user message: '{last_user_message}'")

    # --- Modification Example ---
    # Add a prefix to the system instruction
    original_instruction = llm_request.config.system_instruction or types.Content(role="system", parts=[])
    prefix = "[Modified by Callback] "
    # Ensure system_instruction is Content and parts list exists
    if not isinstance(original_instruction, types.Content):
        original_instruction = types.Content(role="system", parts=[types.Part(text=str(original_instruction))])
    if not original_instruction.parts:
        original_instruction.parts.append(types.Part(text=""))  # Add an empty part if none exist

    # Modify the text of the first part
    modified_text = prefix + (original_instruction.parts[0].text or "")
    original_instruction.parts[0].text = modified_text
    llm_request.config.system_instruction = original_instruction
    print(f"[Callback] Modified system instruction to: '{modified_text}'")

    # --- Skip Example ---
    # Check if the last user message contains "BLOCK"
    if "BLOCK" in last_user_message.upper():
        print("[Callback] 'BLOCK' keyword found. Skipping LLM call.")
        # Return an LlmResponse to skip the actual LLM call
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="LLM call was blocked by before_model_callback.")],
            )
        )
    else:
        print("[Callback] Proceeding with LLM call.")
        # Return None to allow the (modified) request to go to the LLM
        return None


# Create LlmAgent and Assign Callback
my_llm_agent = LlmAgent(
        name="ModelCallbackAgent",
        model=GEMINI_2_FLASH,
        instruction="You are a helpful assistant.",  # Base instruction
        description="An LLM agent demonstrating before_model_callback",
        before_model_callback=simple_before_model_modifier  # Assign the function here
)

APP_NAME = "guardrail_app"
USER_ID = "user_1"
SESSION_ID = "session_001"

# Session and Runner
async def setup_session_and_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=my_llm_agent, app_name=APP_NAME, session_service=session_service)
    return session, runner


# Agent Interaction
async def call_agent_async(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    session, runner = await setup_session_and_runner()
    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    async for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response: ", final_response)

# Note: In Colab, you can directly use 'await' at the top level.
# If running this code as a standalone Python script, you'll need to use asyncio.run() or manage the event loop.
await call_agent_async("write a joke on BLOCK")
```
---

### By understanding this mechanism of returning `None` versus returning `specific objects`, you can precisely control the agent's execution path, making callbacks an essential tool for building sophisticated and reliable agents.

