from google.adk.runners import Runner
from multi_tool_agent import root_agent


def create_runner(app_name, session_service):
    """
    Create the ADK runner responsible for executing the agent.
    """

    return Runner(
        agent=root_agent,
        app_name=app_name,
        session_service=session_service,
    )