from google.adk.agents import Agent

root_agent = Agent(
    name="conversation_context_agent",
    model="gemini-2.5-flash",
    description="Agent for verifying conversation context reconstruction and event compaction.",
    instruction=(
    "You are a conversational assistant. "
    "Answer naturally using only the information available in the current conversation history. "
    "Remember details shared by the user during the conversation and use them when answering follow-up questions. "
    "If information has not been shared during the conversation, say that you do not know instead of making assumptions."
    ),
)