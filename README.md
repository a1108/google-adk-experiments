# Google ADK Engineering Lab

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Google ADK](https://img.shields.io/badge/Google-ADK-4285F4)
![Gemini](https://img.shields.io/badge/Gemini-LLM-8E75B2)
![Vertex AI](https://img.shields.io/badge/Vertex-AI-34A853)
![Status](https://img.shields.io/badge/Status-Active-success)

> A hands-on engineering lab for exploring the Google Agent Development Kit (ADK). Each experiment investigates how ADK works internally through documentation, source code analysis, runtime verification, and database inspection, with every finding backed by practical experimentation.

---

# Why this repository?

Most Google ADK examples demonstrate **how** to build an agent.

This repository focuses on understanding **how Google ADK works internally**.

Each experiment follows the same engineering methodology:

- Read the official documentation
- Explore the ADK source code
- Build a runnable example
- Verify runtime behavior
- Inspect the SQLite database (where applicable)
- Document only verified findings

The objective is to build a deep understanding of AI agent runtime architecture rather than simply producing working examples.

---

# What You'll Learn

This repository explores:

- Runtime Bootstrapping
- Session Management
- Persistent Conversation Memory
- Conversation State
- Event Lifecycle
- Context Management
- Event Compaction
- Token Optimization
- Streaming Responses
- Model Context Protocol (MCP)
- Semantic Routing
- Agent Delegation
- Invocation Lifecycle
- Coordinator Agent Architecture

## Future Explorations

- Long-Term Memory
- Retrieval-Augmented Generation (RAG)
- Production Deployment Patterns

---


# Technologies

- Python 3.14
- Google Agent Development Kit (ADK)
- Google Gemini 2.5 Flash
- Vertex AI
- Google Cloud Platform
- SQLite
- Model Context Protocol (MCP)
- Google Maps MCP Server
- AgentTool

---

# Repository Goals

The objective of this repository is to:

- Explore Google ADK concepts through practical implementation
- Understand the runtime architecture behind ADK
- Document observations from each experiment
- Evaluate production-oriented design patterns
- Build reusable runtime components
- Serve as a reference for future ADK projects

---

# Current Progress

## ✅ Completed

- Custom Runtime Launcher
- Runtime Bootstrapping
- Runner
- Session Management
- In-Memory Session Service
- Persistent Session Management
- Conversation Memory
- Environment Configuration
- Event Lifecycle
- Context Reconstruction
- Event Compaction
- Context Management
- Token Optimization
- Google Maps MCP Integration
- Multi-Agent Coordination using AgentTool
- Google Maps MCP Tool Integration
- Coordinator Agent
- Semantic Routing

---

## 🚧 Next Experiment

- Streaming Responses

> **Current Focus:** Investigating how Google ADK implements streaming responses, emits Partial Events, reconstructs final Events, and manages the complete streaming execution lifecycle.
---

# Experiment Roadmap

| Experiment | Status |
|------------|:------:|
| ✅ Experiment 01 – Building a Custom ADK Runtime | Completed |
| ✅ Experiment 02 – Implementing Persistent Session Management | Completed |
| ✅ Experiment 03 – Understanding Conversation State | Completed |
| ✅ Experiment 04 – Understanding Event Lifecycle | Completed |
| ✅ Experiment 05 – Context Management & Token Optimization | Completed |
| 🚧 Experiment 06 – Streaming Responses | In Progress |
| ✅ Experiment 07 – Google Maps MCP Integration | Completed |
| ✅ Experiment 08 – Multi-Agent Coordination using AgentTool | Completed |
---

# Engineering Principles

The implementation in this repository follows these principles:

- Single Responsibility Principle (SRP)
- Separation of Concerns
- Modular Runtime Design
- Reusable Components
- Production-Oriented Architecture
- Incremental Experimentation

---

# Verification Philosophy

Every conclusion in this repository is based on evidence rather than assumptions.

Whenever possible, findings are verified through:

- Official Google ADK documentation
- ADK source code analysis
- Runtime experiments
- SQLite database inspection

Only verified observations are documented.

Each experiment validates findings by comparing runtime behavior with the Google ADK source code to ensure conclusions accurately reflect the framework's implementation.

---

# Runtime Architecture

The following diagram illustrates the high-level runtime architecture used throughout the experiments.

```text
                 User
                  │
                  ▼
         python -m launcher.run
                  │
                  ▼
            bootstrap.py
                  │
      ┌───────────┼────────────┐
      ▼           ▼            ▼
   env.py     session.py    runner.py
      │           ▲            │
      ▼           │            ▼
Vertex AI Config  │     Runner Execution
                  │            │
                  └────────────┘
                       │
                       ▼
              DatabaseSessionService
                       │
                       ▼
                 SQLite Database
                       │
                       ▼
                  Session Events
                       │
                       ▼
          Context Reconstruction
                       │
                       ▼
             Event Compaction (Optional)
                       │
                       ▼
                Coordinator Agent
                        │
                        ├──────────────┐
                        ▼              ▼
                  Conversation     Google Maps
                  Context Agent     MCP Agent
                        │              │
                        └──────┬───────┘
                               ▼
                           Gemini Model
                               │
                               ▼
                          Final Response
```                          
                         

---

# Project Structure

```text
.
│
├── launcher/
│   ├── __init__.py
│   ├── console.py
│   └── run.py
│
├── runtime/
│   ├── __init__.py
│   ├── bootstrap.py
│   ├── config.py
│   ├── context.py
│   ├── env.py
│   ├── logger.py
│   ├── runner.py
│   └── session.py
│
├── experiments/
│   ├── Experiment-01-Building-a-Custom-ADK-Launcher.md
│   ├── Experiment-02-Implementing-Persistent-Session-Management.md
│   ├── Experiment-03-Understanding-Conversation-State.md
│   ├── Experiment-04-Understanding-Event-Lifecycle.md
│   ├── Experiment-05-Context-Management-and-Token-Optimization.md
│   ├── Experiment-05–Runtime-Verification-of-Event-Compaction.md
│   ├── Experiment-07-Google-Maps-MCP-Integration.md
│   └── Experiment-08-Multi-Agent-Coordination-using-AgentTool.md
│
├── data/
│
├── multi_tool_agent/
│   ├── __init__.py
│   └── agent.py
│
├── common/
│   ├── __init__.py
│   ├── agent.py
│   └── coordinator/
│       ├── __init__.py
│       └── agent.py
│
├── context_agent/
│   ├── __init__.py
│   └── agent.py
│
├── mcp_integration/
│   ├── __init__.py
│   └── agent.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Getting Started

## Clone the Repository

```bash
git clone https://github.com/a1108/google-adk-experiments.git
cd google-adk-experiments
```

---

## Create a Virtual Environment

```bash
python -m venv .venv
```

---

## Activate the Virtual Environment

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```cmd
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Copy `.env.example` to `.env` and update the required values.

Example:

```properties
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your-project-id>
GOOGLE_CLOUD_LOCATION=us-central1
```

---

# Running the Application

Launch the custom runtime:

### Custom Runtime

```bash
python -m launcher.run
```

### ADK Web

```bash
adk web
```

The custom runtime automatically:

- Loads environment variables
- Initializes the session service
- Loads or creates a conversation session
- Creates the ADK Runner
- Starts the interactive console

---

# Experiment Index

Each experiment builds upon previous work and explores one architectural concept in Google ADK.

Every experiment documents:

- Objective
- Research Questions
- Runtime Verification
- Architecture / Runtime Flow
- Findings
- Verification Checklist
- References

| Experiment | Status |
|------------|:------:|
| Experiment 01 – Building a Custom ADK Runtime | ✅ |
| Experiment 02 – Persistent Session Management | ✅ |
| Experiment 03 – Understanding Conversation State | ✅ |
| Experiment 04 – Understanding Event Lifecycle | ✅ |
| Experiment 05 – Context Management & Token Optimization | ✅ |
| Experiment 06 – Streaming Responses | 🚧 |
| Experiment 07 – Google Maps MCP Integration | ✅ |
| Experiment 08 – Multi-Agent Coordination using AgentTool | ✅ |

---

# Experiment Methodology

Every concept in this repository follows the same engineering process.

```text
Read Documentation
        │
        ▼
Explore Source Code
        │
        ▼
Build Experiment
        │
        ▼
Run & Verify
        │
        ▼
Inspect Runtime
        │
        ▼
Document Findings
```

The focus is on understanding the underlying architecture rather than simply building a working example.

---

# Repository Highlights

✔ Built a custom Google ADK runtime

✔ Explored ADK runtime architecture through engineering experiments

✔ Implemented persistent conversation memory

✔ Investigated Event Lifecycle, Context Reconstruction, Event Compaction and Token Optimization

✔ Built a Google Maps MCP specialist agent

✔ Implemented a Coordinator Agent using AgentTool

✔ Verified semantic routing using ADK Trace

✔ Investigated Invocation lifecycle during delegated agent execution

✔ Structured the repository as an engineering lab instead of isolated examples

---

# References

- Google Agent Development Kit (ADK) Documentation
- Google ADK GitHub Repository
- Google Gemini Documentation
- Vertex AI Documentation
- Model Context Protocol Specification

---

# What's Next?

Upcoming experiments will explore:

- Streaming Responses
- Long-Term Memory
- Retrieval-Augmented Generation (RAG)
- Production Deployment Patterns
- Advanced Multi-Agent Workflows

---

# License

This repository is intended for educational purposes, experimentation, and knowledge sharing.

Feel free to explore the code, learn from the experiments, and adapt the ideas for your own projects.