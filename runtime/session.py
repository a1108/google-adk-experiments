from google.adk.sessions import InMemorySessionService


async def create_session(
    app_name: str,
    user_id: str,
    session_id: str,
):
    """
    Create and initialize an ADK conversation session.

    Returns:
        tuple:
            session_service (InMemorySessionService): Manages conversation sessions.
            session: Represents the current user conversation.
    """

    # Create the session manager.
    session_service = InMemorySessionService()

    # Create a new conversation session.
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )

    print(
        f"Session created: "
        f"App='{app_name}', "
        f"User='{user_id}', "
        f"Session='{session_id}'"
    )

    # Return both the session manager and the newly created session.
    return session_service, session