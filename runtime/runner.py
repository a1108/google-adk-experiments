from google.adk.runners import Runner
#from multi_tool_agent import root_agent
from context_agent import root_agent
from google.adk.apps import App
from google.adk.apps._configs import EventsCompactionConfig


def create_runner(app_name, session_service):
    """
    Create the ADK runner responsible for executing the agent.
    """
    app = App(
        name=app_name,
        root_agent=root_agent,
        events_compaction_config=EventsCompactionConfig(
            token_threshold=300,
            event_retention_size=2,
            compaction_interval=2,
            overlap_size=1,
        ),
    )

    return Runner(
        app=app,
        session_service=session_service,
    )