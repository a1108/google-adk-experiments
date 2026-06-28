# Experiment 05 – Runtime Verification of Event Compaction (Evidence)

## Objective

This document captures the runtime evidence collected while performing Experiment 05 – Runtime Verification of Event Compaction.

Unlike the theory document, which explains how Event Compaction works internally, this document focuses on runtime verification. Every observation presented here is supported by evidence collected during the experiment, including runtime logs, SQLite events, LLM requests, and conversation validation.

The primary objectives of this experiment were to verify:

* Event Compaction is triggered after the configured token threshold is exceeded.
* Google ADK generates and persists a Compaction Event.
* The generated summary preserves important conversation context.
* Future prompts are reconstructed using the generated summary.
* Conversation continuity is maintained after Event Compaction.
* Event Compaction survives an application restart.

⸻

## Experiment Configuration

The following configuration was used throughout this experiment:

EventsCompactionConfig(
    token_threshold=300,
    event_retention_size=2,
    compaction_interval=2,
    overlap_size=1,
)

⸻

## Verification Summary

| # | Expectation | What We Observed | Conclusion |
|---|-------------|------------------|------------|
| 1 | Event Compaction should become active once the conversation crosses the configured token threshold. | During the second invocation, the prompt reached **368 tokens**, exceeding the configured `token_threshold = 300`. | ✅ **Verified** → [Proof 1](#proof-1) |
| 2 | ADK Runner Executed Event Compaction. | Runtime logs showed **"Running event compactor."** followed by **"Token-threshold event compactor finished."** | ✅ **Verified** → [Proof 2](#proof-2) |
| 3 | Event Compaction Generated a Dedicated Compaction Event | SQLite recorded a new Event containing `actions.compaction` with a generated conversation summary. | ✅ **Verified** → [Proof 3](#proof-3) |
| 4 | The generated summary should preserve the important information shared during the conversation. | The generated summary captured the user's identity, profession, technical interests, current project, and long-term career goal. | ✅ **Verified** → [Proof 4](#proof-4) |
| 5 | Future conversations should use the generated summary instead of replaying the original conversation history. | The LLM request contained **"For context:"** followed by the generated summary instead of replaying the original conversation events. | ✅ **Verified** → [Proof 5](#proof-5) |
| 6 | Conversation Continuity Was Maintained | The agent correctly recalled the user's profile, interests, project, and career goal without requiring the information to be repeated. | ✅ **Verified** → [Proof 6](#proof-6) |
| 7 | Event Compaction should survive an application restart. | After restarting the application, the existing SQLite session was restored and the agent continued using the previously generated summary. | ✅ **Verified** → [Proof 7](#proof-7) |
| 8 | Runtime Behavior Matched the Expected ADK Execution Flow. | Runtime logs, LLM requests, SQLite events, and observed execution all followed the expected Event Compaction lifecycle. | ✅ **Verified** → [Proof 8](#proof-8) |
| 9 | `event_retention_size = 2` should preserve recent conversation while summarizing older conversation. | Runtime observations were consistent with this behavior, although the exact retention behavior was not independently isolated during this experiment. | 🟡 **Partially Verified** → [Proof 9](#proof-9) |
| 10 | `overlap_size = 1` should influence how consecutive compaction windows share context. | The parameter was configured successfully, but its isolated behavior could not be verified because only one configuration was evaluated during this experiment. | ⏳ **Future Verification** → [Proof 10](#proof-10) |
⸻

## Experiment Timeline

Phase	Description	Evidence
Phase 1	Initial conversation established between the user and the agent.	Events 1–4
Phase 2	After the configured token threshold was exceeded, ADK automatically generated the first Compaction Event.	Event 5
Phase 3	The application was restarted, and the existing session was restored from SQLite. The agent reconstructed the conversation using the generated summary.	Events 6–7
Phase 4	As the conversation continued, ADK generated an updated Compaction Event containing the latest summarized context.	Event 8

⸻

## Proofs

The following sections contain the runtime evidence collected during the experiment. Each proof includes the original runtime artifacts exactly as they were captured, followed by the observations and conclusions derived from them.

### Proof 1 - Event Compaction Became Eligible

#### Expectation

Event Compaction should not execute immediately after the conversation starts. Instead, the conversation must first exceed the configured token_threshold. Only after crossing this threshold should the Runner consider the conversation eligible for compaction.

#### Runtime Evidence

The first invocation established the initial conversation between the user and the agent.

Event 1 – User Message
```json
{
  "content": {
    "parts": [
      {
        "text": "My name is Ankit Gupta. I live in Delhi, India. I work as a Senior Software Engineer. I primarily develop backend applications using Java, Spring Boot, and Microservices. I enjoy learning Google ADK, AI Agents, Kafka, and System Design. I am currently building an engineering repository to understand how Google ADK works internally through documentation, source code analysis, runtime verification, and SQLite database inspection. Please remember these details because I will ask you about them later in this conversation."
      }
    ],
    "role": "user"
  },
  "usage_metadata": null
}
```

Event 2 – Agent Response

```json
{
  "usage_metadata": {
    "prompt_token_count": 191,
    "candidates_token_count": 105,
    "total_token_count": 331
  }
}
```
At the end of the first invocation, the prompt contained 191 tokens, which is below the configured threshold of 300 tokens.

The second invocation introduced additional information about production architecture, distributed systems, Redis, Kafka, database indexing, event-driven architecture, observability, and the user’s long-term career goal.

Event 3 – User Message

```json
{
  "content": {
    "parts": [
      {
        "text": "I am also interested in production architecture and distributed systems..."
      }
    ],
    "role": "user"
}
```

Event 4 – Agent Response

```json
{
  "usage_metadata": {
    "prompt_token_count": 368,
    "candidates_token_count": 95,
    "total_token_count": 510
  }
}
```

#### Observation

The prompt size increased from:

* Invocation 1: 191 tokens
* Invocation 2: 368 tokens

Since the configured threshold was 300 tokens, the second invocation exceeded the threshold, making the conversation eligible for Event Compaction.

#### Conclusion

The runtime evidence confirms that Event Compaction became eligible only after the configured token threshold was exceeded.

⸻

### Proof 2 - ADK Generated the First Compaction Event

#### Expectation

Once the configured token threshold is exceeded, the ADK Runner should execute the Event Compaction framework and generate a dedicated Compaction Event instead of modifying the original conversation events.

#### Runtime Evidence

Immediately after the second invocation completed, a new event appeared in the SQLite events table.

Unlike the previous conversation events, this event did not contain normal user or model content. Instead, it contained a new actions.compaction object.

Event 5 – First Compaction Event

```json
{
  "actions": {
    "compaction": {
      "start_timestamp": 1782640904.179583,
      "end_timestamp": 1782640904.193152,
      "compacted_content": {
        "parts": [
          {
            "text": "**User Request:** The user explicitly asked the AI to remember the provided personal and project details for future reference in the conversation.\n\n**Context Summary:**\n* User Identity: Ankit Gupta\n* Profession: Senior Software Engineer\n* Interests: Google ADK, AI Agents, Kafka and System Design\n* Current Project: Engineering repository for Google ADK\n..."
          }
        ]
      }
    }
  }
}
```

#### Observation

This event differs significantly from the previous conversation events.

Instead of storing another user or model message, ADK generated a dedicated Compaction Event containing a summarized representation of the conversation.

The original conversation events remained unchanged, while the summary was persisted as a new event.

#### Conclusion

The SQLite database confirms that ADK generated a dedicated Compaction Event after the configured token threshold was exceeded.

⸻

### Proof 3 - Important Conversation Context Was Preserved

#### Expectation

Generating a summary is only useful if it preserves the important information shared during the conversation. The Compaction Event should therefore capture the essential context instead of simply shortening the conversation.

Runtime Evidence

The generated Compaction Event contained the following summarized information.

User Identity:
Ankit Gupta
Profession:
Senior Software Engineer
Interests:
Google ADK
AI Agents
Kafka
System Design
Current Project:
Building an engineering repository to understand Google ADK.
Project Methodology:
• Documentation
• Source Code Analysis
• Runtime Verification
• SQLite Database Inspection

The summary also recorded that the agent had acknowledged and remembered these details for future interactions.

#### Observation

Although the original conversation contained several long messages, the Compaction Event successfully condensed the conversation into a structured summary while preserving all important information required for future context reconstruction.

Rather than replaying the complete conversation history, ADK extracted only the information necessary to continue the conversation naturally.

#### Conclusion

The first Compaction Event demonstrates that Event Compaction is not simply reducing tokens. It is generating a structured summary that preserves the essential conversation context for future interactions.


Excellent. Now we move to the most interesting part of the experiment—the runtime proof that the generated summary was actually used after restarting the application.

### Proof 4 - Conversation Context Was Successfully Reconstructed

#### Expectation

Generating a Compaction Event alone is not sufficient. The real objective of Event Compaction is to reduce the amount of conversation sent to the model while preserving enough context for future interactions.

If Event Compaction is functioning correctly, the agent should be able to answer questions about previously shared information without requiring the user to repeat it.

Runtime Evidence

After the first Compaction Event was generated, the application was stopped and restarted.

The existing SQLite session was loaded successfully, indicating that the previous conversation had been restored.

The user then asked the following question.

Event 6 – User Message

```json
{
  "content": {
    "parts": [
      {
        "text": "Without me repeating anything, tell me everything you remember about me from our previous conversation."
      }
    ],
    "role": "user"
  }
}
```

The agent responded with the following information.

Event 7 – Agent Response

```json
{
  "content": {
    "parts": [
      {
        "text": "Certainly, Ankit. Here's everything I remember about you from our conversation:\n\nYou are Ankit Gupta, a Senior Software Engineer residing in Delhi, India. You specialize in backend development, particularly with Java, Spring Boot, and Microservices.\n\nYour interests include learning Google ADK, AI Agents, Kafka, and System Design. Currently, you are working on a project to build an engineering repository to deeply understand Google ADK. You're achieving this understanding through documentation review, source code analysis, runtime verification, and SQLite database inspection.\n\nAdditionally, you are interested in production architecture and distributed systems. Your studies frequently cover caching strategies, Redis, Kafka consumer groups, database indexing, event-driven architecture, and observability using Datadog and Dynatrace. Your long-term goal is to become an AI Solution Architect capable of designing scalable enterprise systems."
      }
    ]
  }
}
```

#### Observation

The response contained information originating from both conversation phases.

The agent successfully recalled:

* User identity
* Current city
* Profession
* Technical expertise
* Current engineering project
* Technical interests
* Additional interests introduced during the second invocation
* Long-term career goal

Most importantly, none of this information was repeated by the user after restarting the application.

#### Conclusion

The runtime evidence confirms that Event Compaction successfully reconstructed the conversation context, allowing the agent to continue the conversation naturally after the original messages had already been compacted.

⸻

### Proof 5 - ADK Generated an Updated Compaction Event

#### Expectation

Event Compaction should not produce a static summary.

As the conversation continues, Google ADK should regenerate the compacted summary so that newly introduced information also becomes part of the summarized conversation.

#### Runtime Evidence

Following the successful context reconstruction, SQLite recorded another Compaction Event.

Event 8 – Second Compaction Event

```json
{
  "actions": {
    "compaction": {
      "start_timestamp": 1782640904.179583,
      "end_timestamp": 1782641006.261708,
      "compacted_content": {
        "parts": [
          {
            "text": "**User Request:** The user wants the AI to remember additional information about their interests and career goals...\n\n**Context Summary:**\n• User Identity: Ankit Gupta\n• Senior Software Engineer\n• Google ADK engineering repository\n• Production architecture\n• Distributed systems\n• Redis\n• Kafka consumer groups\n• Database indexing\n• Event-driven architecture\n• Datadog\n• Dynatrace\n• Goal: Become an AI Solution Architect"
          }
        ]
      }
    }
  }
}
```

#### Observation

Comparing the first and second Compaction Events reveals an important difference.

The first Compaction Event summarized only the initial conversation.

The second Compaction Event incorporated the additional information shared later in the conversation, including:

* Production Architecture
* Distributed Systems
* Redis
* Kafka Consumer Groups
* Database Indexing
* Event-Driven Architecture
* Datadog
* Dynatrace
* AI Solution Architect career goal

Rather than preserving a fixed summary, ADK regenerated the compacted conversation to reflect the latest conversation state.

#### Conclusion

The runtime evidence demonstrates that Event Compaction continuously evolves with the conversation. As new information becomes important, Google ADK generates an updated Compaction Event, ensuring that future conversations are reconstructed using the most recent summarized context.

⸻

### Proof 6 - End-to-End Runtime Verification

#### Runtime Timeline

The complete execution flow observed during this experiment is summarized below.

Phase	Runtime Evidence	Result
Initial Conversation	Event 1, Event 2	User profile established
Additional Context	Event 3, Event 4	Prompt reached 368 tokens, exceeding the configured threshold
First Event Compaction	Event 5	First summarized conversation persisted to SQLite
Application Restart	Existing session restored	Previous conversation successfully recovered
Context Reconstruction	Event 6, Event 7	Agent recalled previously shared information without repetition
Second Event Compaction	Event 8	Summary regenerated to include the latest conversation

#### Final Observation

Throughout the experiment, every important stage of the Event Compaction lifecycle was directly observable.

The collected runtime evidence demonstrates:

* The conversation exceeded the configured token threshold.
* ADK generated a dedicated Compaction Event.
* The generated summary preserved the important conversation context.
* Conversation continuity was maintained after restarting the application.
* The compacted summary evolved as additional information was introduced during later conversations.

#### Conclusion

This experiment validates the complete runtime lifecycle of Google ADK Event Compaction using runtime observations and SQLite inspection rather than relying solely on documentation or source code. The collected evidence demonstrates that Event Compaction not only reduces conversation history but also preserves meaningful context, enabling long-running conversations to continue naturally across multiple invocations and application restarts.

### Proof 7 - Event Compaction Survived Application Restart

#### Expectation

The generated Compaction Event should be persisted as part of the conversation history. After restarting the application, ADK should restore the existing session and continue using the previously generated summary instead of requiring the conversation to start from scratch.

#### Runtime Evidence

After stopping and restarting the application, the following startup logs were observed.

Bootstrapping application...
.env loaded successfully.
Vertex AI : TRUE
Project   : project-19507156-1790-47be-ab1
Location  : us-central1
Loaded an existing persistent session: session_001
App='weather_app', User='ankit', Session='session_001'
Bootstrap completed.
Weather Agent Started

Immediately after the restart, the following question was asked.

Event 6 – User

Without me repeating anything, tell me everything you remember about me from our previous conversation.

The agent successfully recalled all previously shared information, including details from both conversation phases.

Event 7 – Agent

* User Identity
* Profession
* Technical expertise
* Engineering repository
* Additional technical interests
* Long-term career goal

#### Observation

The application did not create a new session after restarting. Instead, it restored the previously persisted session from SQLite and continued the conversation without requiring any information to be repeated.

#### Conclusion

The runtime evidence confirms that Event Compaction is persisted as part of the conversation history and survives application restarts.

⸻
# Proof 8 - Runtime Behavior Matched the ADK Implementation

#### Expectation

The runtime execution should follow the same sequence implemented by Google ADK. The observations collected from runtime logs, SQLite events, and conversation behavior should all align with the expected Event Compaction lifecycle.

#### Runtime Evidence

The following execution sequence was observed during the experiment.

Runtime Step	Evidence
User conversation recorded	Events 1–4
Prompt exceeded configured threshold	Event 4 (prompt_token_count = 368)
Runner executed Event Compaction	Runtime log: Running event compactor.
Compaction completed	Runtime log: Token-threshold event compactor finished.
Compaction Event persisted	Event 5
Conversation reconstructed	Event 6 and Event 7
Updated Compaction Event generated	Event 8

#### Observation

Every important stage of the Event Compaction lifecycle was observable during runtime.

No step required manual intervention after the configured threshold was exceeded.

The runtime logs, SQLite events, and conversation behavior consistently reflected the expected Event Compaction flow.

#### Conclusion

The collected runtime evidence matches the implementation and expected execution flow of Google ADK Event Compaction.

⸻

### Proof 9 - Verification of event_retention_size = 2

#### Expectation

The event_retention_size configuration is intended to preserve the most recent conversation while allowing older conversation to be summarized.

For this experiment, the configuration was:

event_retention_size = 2

#### Runtime Evidence

During the experiment, the following behavior was observed:

* Older conversation was summarized into the first Compaction Event (Event 5).
* The conversation continued naturally after compaction.
* A second Compaction Event (Event 8) contained both the original summary and the newly introduced information.
* The agent successfully answered questions using both previously summarized information and the most recent conversation.

#### Observation

Although the experiment demonstrated that older conversation was summarized while newer context remained available for conversation reconstruction, the exact internal implementation of the retention algorithm was not independently isolated.

Since only one configuration (event_retention_size = 2) was evaluated, it is not possible to determine precisely which events ADK internally retained versus summarized.

#### onclusion

The runtime observations are consistent with the configured event_retention_size, but the exact retention behavior requires additional controlled experiments where only this parameter is varied.

⸻

### Proof 10 - Verification of overlap_size = 1

#### Expectation

The overlap_size parameter is intended to control how much conversation is shared between consecutive compaction windows.

For this experiment, the configuration was:

overlap_size = 1

#### Runtime Evidence

The experiment successfully verified that:

* The parameter was accepted by the application.
* Event Compaction executed successfully.
* A second Compaction Event (Event 8) was generated after additional conversation.

However, because only a single configuration was evaluated, there was no baseline available for comparison.

### Observation

The runtime confirmed that overlap_size did not prevent Event Compaction from functioning correctly.

However, its individual contribution could not be isolated because all configuration parameters remained constant throughout the experiment.

A controlled comparison using multiple configurations (for example, overlap_size = 0, 1, and 2) would be required to quantify its exact impact on consecutive compaction windows.

#### Conclusion

The parameter was successfully configured and exercised during runtime, but its isolated behavior remains outside the scope of this experiment and will be verified through a dedicated follow-up experiment.