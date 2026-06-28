from google.adk.agents import Agent

root_agent = Agent(
    name="conversation_context_agent",
    model="gemini-2.5-flash",
    description="Agent for verifying conversation context reconstruction and event compaction.",
    instruction=(
    "You are a conversational assistant."
    "Answer general knowledge questions using your own knowledge."
    "For follow-up questions, use the current conversation history to maintain context."
    "If the user asks about something previously discussed use the conversation history."
    "If the user refers to information that has never been mentioned,ask for clarification instead of making assumptions."
    ),
)