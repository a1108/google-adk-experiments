# Google ADK Experiments

> A collection of practical experiments exploring the Google Agent Development Kit (ADK), runtime architecture, and production-ready AI agent development.

---

# About

This repository contains a collection of practical experiments built while exploring the Google Agent Development Kit (ADK).

Each experiment focuses on understanding a specific ADK concept by implementing it from scratch, analyzing its behavior, and documenting the architectural decisions, observations, and key takeaways.

The objective is to build a strong understanding of ADK internals while following clean architecture, modular design, and production-oriented engineering practices.

---

# Technologies

- Python 3.14
- Google Agent Development Kit (ADK)
- Google Gemini
- Vertex AI
- Google Cloud Platform (GCP)
- Model Context Protocol (MCP) *(Upcoming)*

---

# Repository Goals

This repository is designed to:

- Explore Google ADK concepts through practical implementation
- Understand the runtime architecture behind ADK
- Document observations from each experiment
- Evaluate production-oriented design patterns
- Build reusable runtime components
- Serve as a reference for future ADK projects

---

# Current Progress

## ✅ Phase 1 – Runtime Foundations

Completed:

- Custom Runtime Launcher
- Agent Lifecycle
- Runner
- Session Management
- In-Memory Session Service
- Conversation Memory
- Environment Configuration
- Runtime Bootstrapping

**Next Focus**

- Persistent Session Services
- State Management

---

# Experiment Roadmap

## Phase 1 – ADK Foundations ✅

- ✅ Custom Runtime Launcher
- ✅ Agent Lifecycle
- ✅ Runner
- ✅ Session Management
- ✅ In-Memory Session Service
- ✅ Conversation Memory
- ✅ Environment Configuration
- ✅ Runtime Bootstrapping

---

## Phase 2 – ADK Core Concepts

- ⬜ Persistent Session Service
- ⬜ State Management
- ⬜ Streaming Responses
- ⬜ Event Lifecycle
- ⬜ Artifacts

---

## Phase 3 – Model Context Protocol (MCP)

- ⬜ MCP Fundamentals
- ⬜ GitHub MCP
- ⬜ Google Maps MCP
- ⬜ BigQuery MCP
- ⬜ Custom MCP Server

---

## Phase 4 – Advanced Agent Development

- ⬜ Multi-Agent Systems
- ⬜ Agent Communication
- ⬜ Long-Term Memory
- ⬜ RAG Integration
- ⬜ Production Deployment

---

# Design Principles

The implementation in this repository follows these principles:

- Single Responsibility Principle (SRP)
- Separation of Concerns
- Modular Runtime Design
- Reusable Components
- Production-Oriented Architecture
- Incremental Experimentation

---

# Project Structure

```text
Agents/
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
git clone <repository-url>
cd Agents
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

Start the application using:

```bash
python -m launcher.run
```

---

# Experiments

Each experiment focuses on understanding one core Google ADK concept through implementation, experimentation, and documentation.

| Experiment | Status |
|------------|--------|
| Experiment 01 – Building a Custom ADK Launcher | ✅ Completed |
| Experiment 02 – Understanding Session Persistence | ⏳ Planned |
| Experiment 03 – State Management | ⏳ Planned |
| Experiment 04 – Streaming Responses | ⏳ Planned |
| Experiment 05 – MCP Fundamentals | ⏳ Planned |
| Experiment 06 – GitHub MCP | ⏳ Planned |
| Experiment 07 – Google Maps MCP | ⏳ Planned |
| Experiment 08 – Multi-Agent Systems | ⏳ Planned |

---

# Experiment Methodology

Every concept in this repository follows the same engineering process.

```text
Understand the Concept
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

# References

- Google Agent Development Kit (ADK)
- Google Gemini
- Google Vertex AI
- Model Context Protocol (MCP)

---

# License

This repository is intended for learning, experimentation, and knowledge sharing.