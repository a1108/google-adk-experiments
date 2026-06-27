## Experiment
The existing runtime and agent implementation from Experiments 01–03 were reused without modification.

Unlike previous experiments, no application code changes were required. The objective of this experiment was to understand how Google ADK internally creates, processes, and persists Events during a conversation.

The investigation was performed using four complementary verification techniques:

* Official Google ADK documentation
* Google ADK source code analysis
* Runtime execution
* SQLite database inspection

The application was started using:

```bash
python -m launcher.run
```

Multiple conversations involving user messages, tool calls, tool responses, and state updates were executed.

The generated Events were inspected during runtime and directly from the SQLite database to understand their lifecycle, persistence, and relationship with Session and State.

The runtime observations were then verified against the Google ADK source code to confirm the internal implementation.

---

## Result

The experiment successfully validated that:

* ✅ Every user interaction generates one or more immutable Events.
* ✅ A single conversation turn can generate multiple Events.
* ✅ FunctionCall Events and FunctionResponse Events are persisted independently.
* ✅ `state_delta` is attached to the FunctionResponse Event.
* ✅ Events sharing the same `invocation_id` belong to the same conversation turn.
* ✅ Session, User, and Application State are persisted independently.
* ✅ Conversation history is reconstructed from previously stored Events.
* ✅ Runtime observations matched the Google ADK documentation and source code implementation.

---

## Engineering Takeaway

This experiment demonstrates that Google ADK follows an event-driven architecture where every significant interaction during a conversation is represented as an immutable Event.

Rather than directly modifying conversation history, the Runner orchestrates the creation of User, Model, FunctionCall, and FunctionResponse Events, while the Session and SessionService manage persistence and conversation reconstruction.

State changes are handled independently through `state_delta`, allowing mutable conversation state to evolve while preserving a complete chronological record of execution.

This separation between Events, State, Runner, and SessionService enables a modular and extensible runtime architecture that supports persistence, debugging, auditing, and future scalability without coupling business logic to infrastructure concerns.

This experiment establishes the Event model as the foundation for understanding how Google ADK executes, persists, and reconstructs conversations.

---

## Next Experiment

Experiment 05 - Context Management & Token Optimization

Topics to explore:

* How Google ADK reconstructs model context
* Which Events are included in prompts
* Context window management
* Token optimization strategies
* Event selection during prompt construction
* Conversation compaction and history management

---

## Verification Checklist

* ✅ Official Documentation Verified
* ✅ Google ADK Source Code Verified
* ✅ Runtime Behavior Verified
* ✅ SQLite Database Verified
* ✅ Event Lifecycle Verified
* ✅ State Persistence Verified
* ✅ Conversation Reconstruction Verified

---

## Conclusion

This experiment investigated how Google ADK internally represents and manages conversations through Events.

Unlike previous experiments, the focus was not on extending the runtime but on understanding the framework’s internal architecture through documentation, source code analysis, runtime verification, and database inspection.

The experiment confirmed that a single user interaction can produce multiple immutable Events that collectively represent the complete execution lifecycle of a conversation. It also verified the separation between immutable Events and mutable State, demonstrating how Google ADK maintains both an auditable conversation history and an evolving application context.

These findings establish the Event lifecycle as one of the core architectural foundations of Google ADK and provide a clear understanding of how conversations are created, persisted, reconstructed, and maintained throughout the runtime. This understanding provides the foundation for the next experiment on Context Management and Token Optimization.

---
## References

Documentation

* Google ADK Events
* Google ADK Sessions
* Google ADK State Management

Source Code

* `google/adk/events/event.py`
* `google/adk/events/event_actions.py`
* `google/adk/runners/runner.py`
* `google/adk/sessions/session.py`
* `google/adk/sessions/database_session_service.py`

