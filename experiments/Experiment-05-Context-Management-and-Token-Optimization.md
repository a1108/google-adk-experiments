## Experiment

The existing runtime and agent implementation from Experiments 01–04 were reused without modification.

Unlike previous implementation-focused experiments, no application code changes were required. The objective of this experiment was to understand how Google ADK reconstructs model context, manages conversation history, and performs context compaction for long-running conversations.

The investigation was performed using four complementary verification techniques:

* Official Google ADK documentation
* Google ADK source code analysis
* Runtime execution
* SQLite database inspection

The application was started using:

```bash
python -m launcher.run
```

Multiple conversations involving user messages, model responses, tool calls, and tool responses were executed.

The complete execution flow from Runner through Session, prompt construction, context reconstruction, and Event Compaction was traced using the Google ADK source code.

The investigation verified how conversation history is reconstructed, which Event contents are sent to Gemini, how Event metadata is excluded from prompts, and how the built-in Event Compaction framework manages context optimization when explicitly enabled.

The runtime observations were then verified against the Google ADK source code to confirm the internal implementation.

---

## Result

The experiment successfully validated that:

* ✅ Conversation history is reconstructed from persisted Events.
* ✅ Only Event `content` objects are included in the model prompt.
* ✅ Event metadata remains internal and is not sent to Gemini.
* ✅ User, Model, FunctionCall, and FunctionResponse contents are included in the prompt.
* ✅ Partial Events are excluded from conversation history.
* ✅ Google ADK provides a built-in Event Compaction framework.
* ✅ Event Compaction supports both Sliding Window and Token Threshold compaction strategies.
* ✅ Event Compaction executes only when `events_compaction_config` is explicitly configured.
* ✅ Compaction generates summarized Events that are persisted through the SessionService.
* ✅ Runtime observations matched the Google ADK documentation and source code implementation.

---

## Engineering Takeaway

This experiment demonstrates that Google ADK reconstructs model context from persisted conversation Events rather than maintaining a separate prompt history.

Before each model invocation, the framework extracts the `content` from previously stored Events while excluding Event metadata such as identifiers, timestamps, invocation IDs, and state information. This allows the model to receive only the information required for reasoning while preserving complete execution metadata for persistence and auditing.

The investigation also confirmed that Google ADK provides a configurable Event Compaction framework for context management and token optimization. By default, the runtime preserves the complete conversation history. When an `EventsCompactionConfig` is supplied, the Runner invokes the compaction framework after each completed invocation, allowing summarized Events to be generated and persisted while reducing the effective conversation context sent to future model requests.

This experiment establishes Context Reconstruction and Event Compaction as key architectural mechanisms that enable scalable, long-running conversations in Google ADK.”

---

## Next Experiment

Experiment 06 - Streaming Responses

Topics to explore:

* Streaming response lifecycle
* Incremental Event generation
* Partial Events
* Streaming execution flow
* Runner streaming architecture
* Real-time response handling

---

## Verification Checklist

* ✅ Official Documentation Verified
* ✅ Google ADK Source Code Verified
* ✅ Runtime Behavior Verified
* ✅ SQLite Database Verified
* ✅ Context Reconstruction Verified
* ✅ Prompt Construction Verified
* ✅ Event Compaction Framework Verified
* ✅ Sliding Window Compaction Verified
* ✅ Token Threshold Compaction Verified
* ✅ Runner Compaction Execution Path Verified

---

## Conclusion

This experiment investigated how Google ADK reconstructs conversation context and manages long-running conversations through its built-in Event Compaction framework.

Unlike previous implementation-focused experiments, the objective was to understand the framework's internal architecture through documentation, source code analysis, runtime verification, and database inspection.

The investigation confirmed that conversation history is reconstructed from persisted Events by extracting only their `content` while excluding internal Event metadata from model prompts. It also verified that Google ADK includes a configurable Event Compaction framework capable of performing Sliding Window and Token Threshold compaction to optimize conversation context. These capabilities are disabled by default and become active only when an `EventsCompactionConfig` is explicitly configured.

These findings establish Context Reconstruction and Event Compaction as core architectural mechanisms within Google ADK, explaining how conversation history is reconstructed, optimized, and maintained throughout long-running interactions. This understanding provides the foundation for the next experiment on Streaming Responses.

---

## References

### Documentation

* Google ADK Sessions
* Google ADK Events
* Google ADK Event Compaction

### Source Code

* google/adk/runners.py
* google/adk/sessions/session.py
* google/adk/events/event.py
* google/adk/apps/compaction.py
* google/adk/apps/_configs.py
* google/adk/apps/llm_event_summarizer.py