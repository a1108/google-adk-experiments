import asyncio

from runtime.env import load_environment
from runtime.session import get_or_create_session
from runtime.runner import create_runner

from runtime.config import APP_NAME
from runtime.context import USER_ID
from runtime.context import SESSION_ID
from runtime.logger import configure_logging

def bootstrap():
    """
    Initialize the complete ADK runtime.

    Returns:
        tuple:
            runner
            session
    """

    print("Bootstrapping application...")

    # Initialize logging.
    configure_logging()

    # Load environment variables.
    load_environment()

    # Create SessionService and Session.
    session_service, session = asyncio.run(
        get_or_create_session(
            APP_NAME,
            USER_ID,
            SESSION_ID,
        )
    )

    # Create Runner.
    runner = create_runner(
        APP_NAME,
        session_service,
    )

    print("Bootstrap completed.")

    return runner, session