# Experiment 02 - Implementing Persistent Session Management

# Objective

Experiment 01 introduced a custom runtime responsible for bootstrapping the Google ADK application.

The runtime successfully initialized the SessionService, Session, Runner, and launched the agent without relying on adk web.

However, the application still used InMemorySessionService, which stores conversation history only while the application is running.

The objective of this experiment is to implement persistent conversation management in Google ADK by replacing the default in-memory session service with a database-backed session implementation while preserving the existing runtime architecture.

⸻

# Problem Statement

During Experiment 01, the runtime created a new session every time the application started.

```text
Application Start
        │
        ▼
Create InMemorySessionService
        │
        ▼
Create Session
        │
        ▼
Conversation
        │
        ▼
Application Stops
        │
        ▼
Conversation Lost
```

Although the agent could remember information during execution, restarting the application always resulted in a completely new conversation.

The objective of this experiment is to persist conversations so that previously created sessions can be restored automatically after the application restarts.

⸻

# Solution

The runtime was updated to replace:

```python
InMemorySessionService()
```

with:

```python
DatabaseSessionService(db_url="sqlite+aiosqlite:///data/session.db")
```

Instead of always creating a new session, the runtime now:

1. Attempts to load an existing session.
2. Creates a new session only when one does not already exist.

This allows conversations to continue seamlessly across multiple application executions.

⸻

## Session Lifecycle

```text
Application Start
        │
        ▼
Create DatabaseSessionService
        │
        ▼
Load Existing Session
        │
   ┌────┴─────┐
   │          │
 Found    Not Found
   │          │
Reuse    Create Session
   │          │
   └────┬─────┘
        ▼
Create Runner
        │
        ▼
Start Console
        │
        ▼
User Interaction
        │
        ▼
Events Persisted
        │
        ▼
Application Stops
        │
        ▼
Restart Application
        │
        ▼
Load Existing Session
```
⸻

# Runtime Architecture

Only the SessionService implementation changed.

The overall runtime architecture remains unchanged.

```text
run.py
   │
   ▼
bootstrap.py
   │
   ├────────────┬──────────────┬────────────────┐
   ▼            ▼              ▼                ▼
logger.py    env.py      session.py      runner.py
                              │                │
                              ▼                │
                  DatabaseSessionService       │
                              │                │
                              ▼                │
                           SQLite             │
                              │                │
                              ▼                │
                           Session            │
                                               ▼
                                       multi_tool_agent
                                               │
                                               ▼
                                            root_agent
                                               │
                                               ▼
                                            Gemini
                                               │
                                               ▼
                                              Tools
```
⸻

# Project Structure

```text
launcher/
    run.py
    console.py
runtime/
    bootstrap.py
    config.py
    context.py
    env.py
    logger.py
    runner.py
    session.py
data/
    session.db
multi_tool_agent/
    agent.py
```
⸻

# Responsibilities

session

Responsible for:

* Creating the DatabaseSessionService
* Loading an existing session
* Creating a new session when one does not already exist
* Returning both the SessionService and Session to the runtime

⸻

# DatabaseSessionService

Responsible for:

* Persisting conversation history
* Retrieving existing conversations
* Managing session storage
* Automatically creating the SQLite database when required

⸻

# Experiment

The application was started using:

```bash
python -m launcher.run
```

The runtime successfully:

* Loaded environment variables
* Initialized Vertex AI authentication
* Created the DatabaseSessionService
* Loaded an existing session (or created a new one when necessary)
* Created the ADK Runner
* Started the interactive console

Conversation persistence was validated using the following sequence:

1. Start the application.
2. Introduce user information.
3. Stop the application.
4. Restart the application.
5. Continue the previous conversation.

The agent successfully restored the previous conversation without requiring any changes to the agent implementation.

⸻

# Observations

Observation 1

Conversation persistence is achieved by changing the SessionService implementation.

The agent implementation remains completely unchanged.

⸻

Observation 2

Google ADK cleanly separates runtime infrastructure from business logic.

Session management is handled entirely by the runtime while the agent focuses only on conversation logic.

⸻

Observation 3

A persistent conversation is uniquely identified by:

* Application Name
* User ID
* Session ID

Reusing these identifiers allows previously stored conversations to be restored.

⸻

Observation 4

The correct session lifecycle is:

* Load an existing session.
* Create a new session only when one does not already exist.

This prevents duplicate sessions while preserving conversation history.

⸻

Observation 5

This experiment demonstrates the benefit of separation of concerns.

The runtime infrastructure evolved from transient to persistent session management without requiring any modifications to the Runner, Agent, or business logic.

⸻

# Key Learnings

This experiment helped me understand:

* The difference between transient and persistent session storage.
* How Google ADK manages conversation persistence.
* The lifecycle of session retrieval and session creation.
* The responsibility of DatabaseSessionService.
* Why persistent conversations depend on Application Name, User ID, and Session ID.
* How runtime infrastructure can evolve independently from agent implementation.
* The importance of designing runtime components with clear separation of responsibilities.

⸻

# Result

The runtime now successfully restores conversations across application restarts.

The experiment successfully validated that:

* ✅ Existing sessions are automatically restored.
* ✅ New sessions are created only when required.
* ✅ Conversation history survives application restarts.
* ✅ Runtime architecture remains unchanged.
* ✅ Business logic remains completely independent of session persistence.

Example:

```text
First Run

You   : My name is Ankit.
Agent : Hello Ankit.

Application stopped.

Second Run

You   : What is my name?
Agent : Your name is Ankit.

```

This demonstrates that conversation context survives application shutdown and restart using DatabaseSessionService.

⸻

# Engineering Takeaway

This experiment demonstrates one of the key architectural principles of Google ADK:

Conversation persistence is an infrastructure concern rather than an agent concern.

By abstracting session management behind SessionService, ADK allows different storage implementations to be introduced without modifying the agent or execution pipeline.

This separation enables applications to evolve from local development to production-ready persistent storage with minimal code changes.

⸻

# Next Experiment

Experiment 03 - Understanding Conversation State

Topics to explore:

* Difference between Session and State
* State lifecycle
* Event history
* Conversation timeline
* How Google ADK reconstructs context from stored events
* Sharing state across multiple agent interactions

⸻

## Verification Checklist

- ✅ Documentation Verified
- ✅ Source Code Verified
- ✅ Runtime Verified
- ✅ SQLite Database Verified


## Conclusion

This experiment confirmed that replacing `InMemorySessionService` with `DatabaseSessionService` enables persistent conversations without changing the Agent or Runner.

The runtime successfully restored previous conversations across application restarts, demonstrating the separation between conversation persistence and business logic.

## References

### Documentation

- Google ADK Sessions
- Google ADK DatabaseSessionService

### Source Code

- `google/adk/sessions/database_session_service.py`
- `google/adk/sessions/session.py`