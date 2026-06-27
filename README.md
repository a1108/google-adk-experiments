# Google ADK Engineering Lab

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Google ADK](https://img.shields.io/badge/Google-ADK-4285F4)
![Gemini](https://img.shields.io/badge/Gemini-LLM-8E75B2)
![Vertex AI](https://img.shields.io/badge/Vertex-AI-34A853)
![Status](https://img.shields.io/badge/Status-Active-success)

> A hands-on engineering exploration of the Google Agent Development Kit (ADK), where each experiment investigates how ADK works internally through documentation, source code analysis, runtime verification, and database inspection.

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
- Token Optimization
- Streaming Responses
- Model Context Protocol (MCP)
- Multi-Agent Systems

## Future Explorations

- Long-Term Memory
- Retrieval-Augmented Generation (RAG)
- Production Deployment Patterns

---


# Technologies

- Python 3.14
- Google Agent Development Kit (ADK)
- Google Gemini
- Vertex AI
- Google Cloud Platform (GCP)
- SQLite
- Model Context Protocol (MCP) *(Upcoming)*

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

---

## 🚧 Next Experiment

- Context Management & Token Optimization

Current focus: Understanding how Google ADK reconstructs model context, selects Events for prompts, and optimizes token usage.
---

# Experiment Roadmap

| Experiment | Status |
|------------|:------:|
| ✅ Experiment 01 – Building a Custom ADK Runtime | Completed |
| ✅ Experiment 02 – Implementing Persistent Session Management | Completed |
| ✅ Experiment 03 – Understanding Conversation State | Completed |
| ✅ Experiment 04 – Understanding Event Lifecycle | Completed |
| 🚧 Experiment 05 – Context Management & Token Optimization | In Progress |
| ⏳ Experiment 06 – Streaming Responses | Planned |
| ⏳ Experiment 07 – Model Context Protocol (MCP) | Planned |
| ⏳ Experiment 08 – Multi-Agent Systems | Planned |
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
              ┌────────┼─────────┐
              ▼        ▼         ▼
          sessions   events   user_states
                       │
                       ▼
                multi_tool_agent
                       │
                       ▼
                  root_agent
                       │
                       ▼
                 Gemini Model
                       │
                       ▼
                Agent Response
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
├── multi_tool_agent/
│   ├── __init__.py
│   └── agent.py
│
├── experiments/
│   ├── Experiment-01-Building-a-Custom-ADK-Launcher.md
│   ├── Experiment-02-Implementing-Persistent-Session-Management.md
│   ├── Experiment-03-Understanding-Conversation-State.md
│   └── Experiment-04-Understanding-Event-Lifecycle.md
│
├── data/
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

```bash
python -m launcher.run
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
| Experiment 05 – Context Management & Token Optimization | 🚧 |
| Experiment 06 – Streaming Responses | ⏳ |
| Experiment 07 – Model Context Protocol (MCP) | ⏳ |
| Experiment 08 – Multi-Agent Systems | ⏳ |

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

✔ Built a custom Google ADK runtime without relying on `adk web`

✔ Implemented persistent conversation memory using `DatabaseSessionService`

✔ Explored Google ADK runtime architecture through practical engineering experiments

✔ Verified Google ADK runtime behavior through official documentation, source code analysis, runtime experiments, and SQLite database inspection

✔ Repository structured as an incremental engineering lab rather than isolated code examples

---

# References

- Google Agent Development Kit (ADK)
- Google Gemini
- Google Vertex AI
- Model Context Protocol (MCP)

---

# What's Next?

Upcoming experiments will explore:

- Context Management & Token Optimization
- Streaming Responses
- Model Context Protocol (MCP)
- Multi-Agent Systems

Future explorations include:

- Long-Term Memory
- Retrieval-Augmented Generation (RAG)
- Production Deployment Patterns

---

# License

This repository is intended for educational purposes, experimentation, and knowledge sharing.

Feel free to explore the code, learn from the experiments, and adapt the ideas for your own projects.