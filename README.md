# Google ADK Engineering Lab

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Google ADK](https://img.shields.io/badge/Google-ADK-4285F4)
![Gemini](https://img.shields.io/badge/Gemini-LLM-8E75B2)
![Vertex AI](https://img.shields.io/badge/Vertex-AI-34A853)
![Status](https://img.shields.io/badge/Status-Active-success)

> A hands-on engineering exploration of the Google Agent Development Kit (ADK), focusing on runtime architecture, session management, state, memory, MCP, and production-ready AI agent development.

---

# Why this repository?

Most Google ADK examples demonstrate **how** to build an agent.

This repository focuses on understanding **how Google ADK works internally**.

Each experiment explores one architectural concept by:

- Understanding the underlying design
- Implementing the feature from scratch
- Observing runtime behavior
- Documenting architectural decisions
- Recording key learnings and engineering takeaways

The objective is to build a deep understanding of AI agent runtime architecture rather than simply producing working examples.

---

# What You'll Learn

This repository explores:

- Runtime Bootstrapping
- Session Management
- Persistent Conversation Memory
- Conversation State
- Event Lifecycle
- Streaming Responses
- Tool Calling
- Model Context Protocol (MCP)
- Multi-Agent Systems
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

---

## 🚧 Currently Exploring

- Conversation State
- Event Lifecycle

---

# Experiment Roadmap

| Experiment | Status |
|------------|:------:|
| ✅ Experiment 01 – Building a Custom ADK Runtime | Completed |
| ✅ Experiment 02 – Implementing Persistent Session Management | Completed |
| 🚧 Experiment 03 – Understanding Conversation State | In Progress |
| ⏳ Experiment 04 – Event Lifecycle | Planned |
| ⏳ Experiment 05 – Streaming Responses | Planned |
| ⏳ Experiment 06 – Tool Calling | Planned |
| ⏳ Experiment 07 – Model Context Protocol (MCP) | Planned |
| ⏳ Experiment 08 – Multi-Agent Systems | Planned |
| ⏳ Experiment 09 – Long-Term Memory | Planned |
| ⏳ Experiment 10 – RAG Integration | Planned |
| ⏳ Experiment 11 – Production Deployment | Planned |

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
      ┌───────────┼───────────┐
      ▼           ▼           ▼
   env.py     session.py   runner.py
      │           │           │
      │           ▼           │
      │  DatabaseSessionService
      │           │
      │           ▼
      │       SQLite DB
      │
      ▼
 multi_tool_agent
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
│   └── Experiment-02-Implementing-Persistent-Session-Management.md
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

Every experiment includes:

- Objective
- Problem Statement
- Solution
- Architecture
- Observations
- Key Learnings
- Engineering Takeaway

| Experiment | Status |
|------------|:------:|
| Experiment 01 – Building a Custom ADK Runtime | ✅ |
| Experiment 02 – Implementing Persistent Session Management | ✅ |
| Experiment 03 – Understanding Conversation State | 🚧 |
| Experiment 04 – Event Lifecycle | ⏳ |
| Experiment 05 – Streaming Responses | ⏳ |
| Experiment 06 – Tool Calling | ⏳ |
| Experiment 07 – Model Context Protocol (MCP) | ⏳ |
| Experiment 08 – Multi-Agent Systems | ⏳ |

---

# Experiment Methodology

Every concept in this repository follows the same engineering process.

```text
Understand
     │
     ▼
Design
     │
     ▼
Implement
     │
     ▼
Experiment
     │
     ▼
Observe
     │
     ▼
Document
     │
     ▼
Refine
```

The focus is on understanding the underlying architecture rather than simply building a working example.

---

# Repository Highlights

✔ Built a custom Google ADK runtime without relying on `adk web`

✔ Implemented persistent conversation memory using `DatabaseSessionService`

✔ Explored Google ADK runtime architecture through practical engineering experiments

✔ Documented every experiment with architecture diagrams, observations, and engineering takeaways

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

- Conversation State
- Event Lifecycle
- Streaming Responses
- Model Context Protocol (MCP)
- Multi-Agent Collaboration
- Long-Term Memory
- Retrieval-Augmented Generation (RAG)
- Production Deployment Patterns

---

# License

This repository is intended for educational purposes, experimentation, and knowledge sharing.

Feel free to explore the code, learn from the experiments, and adapt the ideas for your own projects.