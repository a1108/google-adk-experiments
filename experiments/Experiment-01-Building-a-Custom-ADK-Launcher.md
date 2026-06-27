# Experiment 01 - Building a Custom ADK Launcher

## Objective

Google ADK provides the `adk web` command to quickly launch an AI agent. While this simplifies development, most of the runtime initialization happens behind the scenes.

The objective of this experiment was to understand how ADK initializes an application by replacing the built-in launcher with a custom runtime implementation.

Instead of relying on `adk web`, this experiment builds the application startup process step by step to understand the responsibilities of each runtime component.

---

# Problem Statement

When launching an ADK application using:

```bash
adk web
```

the following responsibilities are handled automatically:

- Loading environment variables
- Authentication
- Creating the Session Service
- Creating the Session
- Creating the Runner
- Starting the application

Since these steps are abstracted away, it is difficult to understand how ADK works internally.

This experiment recreates these responsibilities programmatically.

---

# Solution

Instead of launching the application using:

```bash
adk web
```

the application is launched using:

```bash
python -m launcher.run
```

A custom runtime is responsible for initializing all infrastructure components before the agent starts executing.

---

# Runtime Architecture

The following diagram illustrates how the application is initialized.

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
                   InMemorySessionService      │
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

---

# Runtime Flow

The following sequence illustrates the complete startup flow.

```text
Application Start
        │
        ▼
python -m launcher.run
        │
        ▼
Bootstrap Runtime
        │
        ├───────────────┐
        │               │
        ▼               ▼
Load Environment   Configure Logger
        │
        ▼
Create Session Service
        │
        ▼
Create Session
        │
        ▼
Create Runner
        │
        ▼
Start Console
        │
        ▼
User Input
        │
        ▼
Runner
        │
        ▼
root_agent
        │
        ▼
Gemini Model
        │
        ▼
Tool Execution
        │
        ▼
Agent Response
```

---

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

multi_tool_agent/
    agent.py
```

---

# Responsibilities

## launcher

Entry point of the application.

Responsible for starting the application.

---

## bootstrap

Coordinates runtime initialization.

Responsibilities include:

- Configure logging
- Load environment variables
- Create SessionService
- Create Session
- Create Runner

---

## env

Loads application configuration from the `.env` file.

---

## logger

Configures application logging and suppresses unnecessary runtime warnings.

---

## session

Creates:

- InMemorySessionService
- Session

---

## runner

Creates the ADK Runner responsible for executing the agent.

---

## console

Provides an interactive console for communicating with the agent.

---

## multi_tool_agent

Contains the business logic of the application.

The agent remains independent of runtime initialization.

---

# Experiment

The application was started using:

```bash
python -m launcher.run
```

The runtime successfully:

- Loaded environment variables
- Initialized Vertex AI authentication
- Created an InMemorySessionService
- Created a Session
- Created the ADK Runner
- Started the interactive console
- Executed the Weather Agent

---

# Observations

## Observation 1

The agent contains only business logic.

Application startup responsibilities belong to the runtime.

---

## Observation 2

The Runner acts as the execution engine.

It receives user requests, invokes the agent, and streams events back to the application.

---

## Observation 3

A Session must exist before a conversation can begin.

The Runner requires:

- SessionService
- Session
- User ID
- Session ID

to maintain conversation context.

---

## Observation 4

Separating runtime components results in a cleaner and more maintainable architecture.

Each module has a single responsibility.

---

## Observation 5

Using `python -m launcher.run` provides complete control over the application startup process compared to relying on `adk web`.

---

# Key Learnings

This experiment helped me understand:

- How ADK initializes an application
- Why bootstrapping is required
- Responsibilities of the Runner
- Difference between Session and SessionService
- Runtime initialization flow
- Environment configuration
- Separation of runtime infrastructure from business logic
- Benefits of modular architecture

---

# Limitations

The current implementation uses `InMemorySessionService`.

Therefore:

- Conversation history exists only while the application is running.
- Restarting the application creates a new session.
- Previous conversations are lost after shutdown.

Persistent sessions will be explored in the next experiment.

---

# Next Experiment

## Experiment 02 – Understanding Session Persistence

Topics to explore:

- Persistent Session Service
- Session lifecycle
- Conversation persistence
- Comparing InMemorySessionService with persistent implementations

---

# Conclusion

This experiment successfully replaced the default `adk web` launcher with a custom runtime implementation.

More importantly, it provided a deeper understanding of the ADK runtime architecture, including bootstrapping, session management, runner initialization, and application startup.

The custom launcher now serves as the foundation for all future experiments in this repository.