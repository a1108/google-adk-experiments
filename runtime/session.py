from google.adk.sessions import DatabaseSessionService
from pathlib import Path


async def get_or_create_session(
    app_name: str,
    user_id: str,
    session_id: str,
):
    """
    Create and initialize an ADK conversation session.

    Returns:
        tuple:
            session_service (DatabaseSessionService): Manages conversation sessions.
            session: Represents the current user conversation.
    """
    # Ensure the data directory exists.
    Path("data").mkdir(exist_ok=True)
    
    # Create the session manager.
    session_service = DatabaseSessionService(db_url="sqlite+aiosqlite:///data/session.db")

    # Try to load an existing session.
    session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )

    # Create a new session only if it doesn't already exist.
    if session is None:
        session = await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
        )
        print(f"Created a new persistent session: {session_id}")
    else:
        print(f"Loaded an existing persistent session: {session_id}")

        print(
            f"App='{app_name}', "
            f"User='{user_id}', "
            f"Session='{session_id}'"
        )

    # Return both the session manager and the newly created session.
    return session_service, session