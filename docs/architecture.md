# Architecture Overview: Prudential Lakehouse Intelligence

## Vision
Prudential Lakehouse Intelligence is a next-generation governance framework that unifies modern Data Engineering principles with the rigor of Lean Six Sigma. The core philosophy is the mapping of the **Medallion Architecture** (Bronze, Silver, Gold) to the **DMAIC** (Define, Measure, Analyze, Improve, Control) methodology, transforming data flows into continuous quality improvement cycles.

## Core Architectural Pillars

### 1. Medallion-DMAIC Mapping
Unlike traditional data lakes, every layer in this lakehouse serves a specific DMAIC purpose:
- **Bronze (Define/Measure):** Raw ingestion and initial data capture.
- **Silver (Analyze):** Cleansed, structured, and enriched data ready for statistical analysis.
- **Gold (Improve/Control):** Highly aggregated, business-ready data that triggers automated quality workflows.

### 2. Event-Driven Quality Intelligence
The architecture moves away from reactive polling towards a proactive, **Event-Driven** model. An internal **Event Bus** monitors changes in the Gold layer, automatically triggering specialized AI agents and quality workflows (e.g., MASP, Kaizen) to detect and remediate deviations in real-time.

### 3. AI Governance & Security-First Design
As the system relies heavily on LLM-powered agents, security is integrated at both the development and runtime layers:
- **Static Security (Development):** Integration of **SkillSpector** in the CI/CD pipeline to scan agent "skills" and tool definitions for vulnerabilities before deployment.
- **Runtime Security (Execution):** A robust **Guardrails** layer that monitors agent behavior, implements Human-in-the-Loop (HITL) for high-impact decisions, and prevents prompt injection.

## Technology Stack
- **API & Orchestration:** FastAPI, LangChain 0.3.
- **Data Engine:** DuckDB (for high-performance analytical processing).
- **Package Management:** Poetry.
- **Security & CI:** SkillSpector, GitHub Actions.
