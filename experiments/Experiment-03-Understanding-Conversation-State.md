# Experiment 03 - Understanding Conversation State

## Objective

Understand why Google ADK provides State even though it already stores the complete conversation history as Events.

This experiment verifies how different State scopes are persisted and managed by Google ADK.

---

## Research Question

- What is State?
- How is State different from Events?
- Where is State stored?
- How does Google ADK persist different State scopes?

---

## Experiment Setup

| Item | Value |
|------|-------|
| Framework | Google ADK |
| Session Service | DatabaseSessionService |
| Database | SQLite |
| Agent | Weather Agent |
| Verification | Documentation + Source Code + Runtime |

---

## Key Concepts

| Events | State |
|--------|-------|
| Stores complete conversation history | Stores important structured data |
| Grows continuously | Usually remains small |
| Used for conversation context | Used for application memory |

---

## State Types

Google ADK determines where State is persisted based on the key prefix used when updating `tool_context.state`.

| Prefix | State Type | Database Table |
|--------|------------|----------------|
| *(No Prefix)* | Session State | `sessions` |
| `user:` | User State | `user_states` |
| `app:` | App State | `app_states` |

---

## Runtime Flow

```text
                     Agent
                       │
                       ▼
              tool_context.state
                       │
                       ▼
             Google ADK Runtime
                       │
                       ▼
               SessionService
                       │
                       ▼
                  SQLite Database
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   sessions       user_states     app_states
(No Prefix)        (user:*)        (app:*)
```

---

## Runtime Verification

Instead of relying only on the documentation, we verified State persistence by writing values into different State scopes and inspecting the SQLite database.

---

## State Persistence Mapping

```text
tool_context.state["current_city"]
                │
                ▼
        sessions.state

tool_context.state["user:name"]
tool_context.state["user:city"]
                │
                ▼
         user_states

tool_context.state["app:weather_api_version"]
                │
                ▼
          app_states
```

---

### State Update Code

```python
# Session State
tool_context.state["current_city"] = city

# User State
tool_context.state["user:name"] = name
tool_context.state["user:city"] = city

# App State
tool_context.state["app:weather_api_version"] = "v1"
```

### Database Verification

| State Written | Verified In |
|---------------|-------------|
| `current_city` | `sessions.state` |
| `user:name` | `user_states` |
| `user:city` | `user_states` |
| `app:weather_api_version` | `app_states` |

---

## Findings

- ✅ Events and State serve different purposes.
- ✅ Session State is stored in the `sessions` table.
- ✅ User State is stored in the `user_states` table.
- ✅ App State is stored in the `app_states` table.
- ✅ The Agent reads and writes State using `tool_context.state`.
- ✅ SessionService persists and retrieves State.

---

## Key Takeaways

- Events preserve the complete conversation history.
- State preserves structured application data.
- State scope is determined by the key prefix.
- Session, User, and App State are persisted in different database tables.
- Runtime verification confirmed the documented behavior of Google ADK State.

---

## Verification Checklist

- ✅ Documentation Verified
- ✅ Source Code Verified
- ✅ Runtime Verified
- ✅ Database Verified

---

## Conclusion

This experiment confirmed that Google ADK persists Session, User, and App State using different storage scopes.

Rather than relying solely on the documentation, these behaviors were verified through source code analysis, runtime experiments, and direct inspection of the SQLite database.

## References

### Documentation

- Google ADK State
- Google ADK Session Management

### Source Code

- `google/adk/sessions/state.py`
- `google/adk/sessions/session.py`
- `google/adk/sessions/database_session_service.py`