# Project Structure — Prudential Lakehouse Intelligence

## Overview

This document describes the complete directory structure and purpose of each component in the Prudential Lakehouse Intelligence project. The structure follows a layered, modular approach aligned with the Medallion Architecture and DMAIC methodology.

## Directory Tree

```
Lakehouse_governance/
├── .github/                          # GitHub configuration
│   └── workflows/
│       └── ci.yml                    # CI/CD pipeline (Security Scan, Lint, Tests)
│
├── ai/                               # AI Agent orchestration & guardrails
│   ├── __init__.py
│   ├── agents/                       # AI agent implementations
│   │   ├── __init__.py
│   │   ├── masp_agent.py             # MASP (Multi-Agent Smart Process) agent
│   │   ├── memory.py                 # Agent memory and state management
│   │   ├── orchestrator.py           # Multi-agent orchestration logic
│   │   ├── quality_agent.py          # Quality domain agent
│   │   └── strategy_planner.py       # Strategic planning agent
│   │
│   ├── guardrails/                   # Security & governance layer
│   │   ├── __init__.py
│   │   ├── action_limits.py          # Rate limiting & action quotas
│   │   ├── hitl.py                   # Human-in-the-Loop mechanisms
│   │   └── permissions.py            # Agent permission model
│   │
│   ├── rag/                          # Retrieval-Augmented Generation
│   │   ├── __init__.py
│   │   ├── generator.py              # LLM response generation
│   │   ├── indexer.py                # Knowledge index creation
│   │   └── retriever.py              # Query-based retrieval pipeline
│   │
│   └── tools/                        # Tool definitions for agents
│       ├── __init__.py
│       ├── data_tools.py             # Data querying & manipulation tools
│       └── quality_tools.py          # Quality-specific tool implementations
│
├── api/                              # REST API & services layer
│   ├── __init__.py
│   ├── config.py                     # API configuration & settings
│   ├── main.py                       # FastAPI application entry point
│   │
│   ├── middleware/                   # HTTP middleware
│   │   ├── __init__.py
│   │   ├── audit.py                  # Audit logging middleware
│   │   └── auth.py                   # Authentication & authorization
│   │
│   ├── routers/                      # API endpoint definitions
│   │   ├── __init__.py
│   │   ├── ai_agent.py               # /api/v1/agents endpoints
│   │   ├── apolices.py               # /api/v1/policies endpoints
│   │   ├── clientes.py               # /api/v1/clients endpoints
│   │   ├── compliance.py             # /api/v1/compliance endpoints
│   │   ├── events.py                 # /api/v1/events endpoints
│   │   └── quality.py                # /api/v1/quality endpoints
│   │
│   ├── schemas/                      # Pydantic request/response models
│   │   ├── __init__.py
│   │   ├── apolice.py                # Policy schema definitions
│   │   ├── cliente.py                # Client schema definitions
│   │   ├── event.py                  # Event schema definitions
│   │   └── quality.py                # Quality metric schema definitions
│   │
│   └── services/                     # Business logic & service layer
│       ├── __init__.py
│       ├── ai_service.py             # AI orchestration service
│       ├── cliente_service.py        # Client data service
│       └── quality_service.py        # Quality management service
│
├── dashboard/                        # Streamlit analytics dashboard
│   ├── __init__.py
│   ├── app.py                        # Main Streamlit application
│   │
│   ├── components/                   # Reusable Streamlit components
│   │   ├── __init__.py
│   │   ├── control_chart.py          # SPC control charts
│   │   ├── ishikawa_diagram.py       # Fishbone diagrams
│   │   ├── kpi_card.py               # KPI display cards
│   │   ├── pareto_chart.py           # Pareto analysis charts
│   │   └── sipoc_table.py            # SIPOC visualization tables
│   │
│   └── pages/                        # Streamlit multi-page app pages
│       ├── __init__.py
│       ├── agent_chat.py             # Agent conversation interface
│       ├── ishikawa.py               # Ishikawa diagram page
│       ├── kaizen.py                 # Kaizen workshop page
│       ├── masp_tracker.py           # MASP process tracker
│       ├── overview.py               # Dashboard overview
│       ├── pareto.py                 # Pareto analysis page
│       └── sipoc.py                  # SIPOC diagram page
│
├── data/                             # Lakehouse medallion layers
│   ├── schema_registry.yaml          # Data schema definitions
│   ├── bronze/                       # Bronze layer (raw data)
│   │   └── [raw data ingestion zone]
│   ├── silver/                       # Silver layer (cleansed data)
│   │   └── [structured, enriched data]
│   └── gold/                         # Gold layer (aggregated analytics)
│       └── [business-ready datasets]
│
├── docs/                             # Project documentation
│   ├── architecture.md               # High-level architecture overview
│   ├── security_scan.md              # Security scanning with SkillSpector
│   ├── sipoc_prudential.md           # SIPOC analysis documentation
│   ├── project_structure.md          # This file - project structure guide
│   │
│   ├── adr/                          # Architecture Decision Records
│   │   ├── 001_medallion_dmaic.md    # ADR: Medallion-DMAIC mapping
│   │   ├── 002_event_bus.md          # ADR: Event-driven architecture
│   │   ├── 003_quality_domain.md     # ADR: Quality domain model
│   │   ├── 004_llm_delta_perception.md # ADR: LLM-based anomaly detection
│   │   └── 005_knowledge_graph.md    # ADR: Knowledge graph implementation
│   │
│   └── diagrams/                     # Architecture diagrams (C4, etc.)
│       └── [Mermaid, Lucidchart, etc.]
│
├── etl/                              # ETL/data pipeline modules
│   ├── __init__.py
│   ├── aggregate.py                  # Data aggregation logic
│   ├── enrich.py                     # Data enrichment pipelines
│   ├── ingest.py                     # Data ingestion modules
│   └── transform.py                  # Data transformation rules
│
├── events/                           # Event-driven architecture
│   ├── __init__.py
│   ├── bus.py                        # Event bus implementation
│   ├── publishers.py                 # Event publisher definitions
│   ├── schemas.py                    # Event schema models
│   └── subscribers.py                # Event subscription handlers
│
├── knowledge/                        # Knowledge management layer
│   ├── __init__.py
│   ├── diagram_vault/                # Quality diagram storage
│   │   └── [ishikawa, pareto, control charts]
│   ├── feature_store/                # Feature engineering layer
│   ├── graph/                        # Knowledge graph storage
│   ├── log_store/                    # Audit & operation logs
│   └── rag_index/                    # RAG vector embeddings & indices
│
├── quality/                          # Quality management frameworks
│   ├── __init__.py
│   ├── dmaic/                        # DMAIC phase implementations
│   ├── iso9001/                      # ISO 9001 compliance modules
│   ├── kaizen/                       # Kaizen continuous improvement
│   ├── masp/                         # MASP (Multi-Agent Smart Process)
│   ├── pdca/                         # PDCA cycle implementations
│   └── tools/                        # Quality analysis tools
│
├── scripts/                          # Standalone utility scripts
│   └── security_scan.py              # SkillSpector security scanning script
│
├── skillspector/                     # Security scanner for AI skills
│   ├── Dockerfile                    # Containerized SkillSpector
│   ├── Makefile                      # Build and testing targets
│   ├── README.md                     # SkillSpector documentation
│   ├── LICENSE                       # Apache 2.0 license
│   ├── SECURITY.md                   # Security policy
│   ├── THIRD_PARTY_NOTICES.md        # Third-party license notices
│   ├── langgraph.json                # LangGraph configuration
│   ├── model_registry.yaml           # LLM model configurations
│   ├── pyproject.toml                # SkillSpector Python project
│   │
│   ├── docs/                         # SkillSpector internal docs
│   │   └── DEVELOPMENT.md            # Developer guide
│   │
│   ├── src/                          # SkillSpector source code
│   │   └── skillspector/
│   │       ├── cli.py                # Command-line interface
│   │       ├── nodes/                # LangGraph analyzer nodes
│   │       └── ...                   # Additional modules
│   │
│   └── tests/                        # SkillSpector test suite
│       └── ...                       # Unit & integration tests
│
├── tests/                            # Project test suite
│   ├── __init__.py
│   ├── test_ai_guardrails.py         # AI security guardrail tests
│   ├── test_etl.py                   # ETL pipeline tests
│   ├── test_events.py                # Event bus tests
│   ├── test_ml.py                    # ML model tests
│   └── test_quality.py               # Quality framework tests
│
├── workflows/                        # Orchestration workflows
│   ├── __init__.py
│   ├── dmaic_pipeline.py             # DMAIC phase orchestration
│   ├── gold_event_handler.py         # Gold layer event handlers
│   ├── kaizen_workflow.py            # Kaizen workshop workflows
│   └── masp_workflow.py              # MASP process workflows
│
├── agent_knowledge_base/             # External knowledge resources
│   └── [Domain-specific knowledge files]
│
├── .github/                          # GitHub-specific files
│   └── workflows/                    # See above
│
├── docker-compose.yml                # Local dev environment (PostgreSQL, etc.)
├── pyproject.toml                    # Main project dependencies (Poetry)
├── README.md                         # Project README
├── scan_report.json                  # Latest security scan report
└── security_report.json              # Generated security scan output
```

## Layer Descriptions

### 1. **Data Layers** (`data/`)
- **Bronze:** Raw data ingestion zone; minimal processing
- **Silver:** Cleansed and enriched data; ready for analysis
- **Gold:** Aggregated, business-ready analytics; triggers events

### 2. **AI/Agents** (`ai/`)
- **Agents:** Multi-agent implementations (MASP, Quality, Strategy)
- **Guardrails:** Security, permissions, Human-in-the-Loop enforcement
- **RAG:** Knowledge retrieval and LLM generation
- **Tools:** Specialized domain tools for agent actions

### 3. **API Layer** (`api/`)
- **Routers:** REST endpoint definitions
- **Schemas:** Request/response validation (Pydantic)
- **Services:** Core business logic and orchestration
- **Middleware:** Auth, audit, cross-cutting concerns

### 4. **Quality Frameworks** (`quality/`)
- **DMAIC:** Define, Measure, Analyze, Improve, Control workflows
- **PDCA:** Plan-Do-Check-Act cycles
- **Kaizen:** Continuous improvement processes
- **MASP:** Multi-Agent Smart Process implementation
- **ISO 9001:** Compliance and standards alignment

### 5. **Event-Driven Architecture** (`events/`)
- **Bus:** Central event routing and subscription management
- **Publishers:** Sources of business events
- **Subscribers:** Event handlers triggering workflows or AI actions

### 6. **ETL Pipelines** (`etl/`)
- **Ingest:** Data source connectors
- **Transform:** Data transformation logic
- **Enrich:** Data enrichment and feature engineering
- **Aggregate:** Statistical and analytical aggregations

### 7. **Knowledge Management** (`knowledge/`)
- **RAG Index:** Vector embeddings and semantic search
- **Feature Store:** Engineered features for ML/analytics
- **Diagram Vault:** Quality diagrams (Ishikawa, Pareto, etc.)
- **Log Store:** Audit trails and operational logs

### 8. **Security & CI/CD** (`skillspector/`, `scripts/`, `.github/`)
- **SkillSpector:** AI skill vulnerability scanner
- **Security Scan Script:** Orchestrates scanning and reporting
- **GitHub Actions:** Automated testing, scanning, and deployment

### 9. **Analytics Dashboard** (`dashboard/`)
- **Streamlit App:** Multi-page analytics interface
- **Components:** Reusable chart and visualization modules
- **Pages:** Domain-specific dashboards (MASP, Kaizen, etc.)

---

## Key Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Project dependencies & Poetry config |
| `docker-compose.yml` | Local environment (PostgreSQL, etc.) |
| `.github/workflows/ci.yml` | CI/CD pipeline (Security, Lint, Tests) |
| `data/schema_registry.yaml` | Data schema definitions |
| `docs/architecture.md` | High-level architecture |
| `docs/architecture_flows.md` | Project architecture and automation flows |
| `docs/adr/` | Architecture decision records |
| `security_report.json` | Latest security scan results |

---

## Development Workflow

1. **Code changes** → Local testing in `tests/`
2. **Push to `develop` or `main`** → Triggers GitHub Actions
3. **CI runs:**
   - Security scan (SkillSpector) → `security_report.json`
   - Linting (Ruff)
   - Unit tests (pytest)
4. **Artifact upload** → `security_report.json` available for review

---

## How to Navigate

- **Want to add a new quality tool?** → See `quality/tools/`
- **Implementing a new API endpoint?** → Add to `api/routers/` and `api/services/`
- **Adding an agent?** → See `ai/agents/` and update orchestrator
- **Understanding the data flow?** → Follow `etl/` → `data/` → `events/` → `workflows/`
- **Visualizing system flows?** → See `docs/architecture_flows.md`

---

*Last updated: 2026-06-21 — Created automatically to document project structure and facilitate navigation.*
