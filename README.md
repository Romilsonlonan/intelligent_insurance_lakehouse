# Prudential Lakehouse Intelligence v2

> **Event-Driven Quality Architecture** — Lean Six Sigma · MASP · ISO 9001 · DMAIC · Kaizen · IA Contextualizada

## Arquitetura

```
Data Sources → Bronze (Medir) → Silver (Analisar) → Gold (Melhorar/Controlar)
                                                          │
                                                    Event Bus (Kafka/FastAPI)
                                                    ┌────┬────────┬──────────┐
                                              Quality  LLM Agent  Memória
                                              Workflow  (Delta)   Org.
                                                    └────┴────────┴──────────┘
                                                          │
                                                    FastAPI (JWT+RBAC+LGPD)
                                                          │
                                                    Dash Dashboard
```

## Módulos principais

| Módulo | Responsabilidade |
|--------|-----------------|
| `etl/` | Ingestão Bronze → Silver → Gold |
| `events/` | Event Bus + schemas de eventos Gold |
| `quality/` | MASP, DMAIC, Kaizen, ISO 9001, Pareto, Ishikawa, SIPOC |
| `ai/` | Orchestrator, MASP Agent, Quality Agent, RAG, Guardrails |
| `knowledge/` | Knowledge Graph (Neo4j), RAG Index, Diagram Vault |
| `workflows/` | Handlers que conectam eventos Gold aos workflows de qualidade |
| `api/` | FastAPI com routers por domínio, JWT+RBAC, audit middleware |
| `dashboard/` | Dash com pages por ferramenta Lean Six Sigma |
| `docs/adr/` | Architecture Decision Records |

## Quickstart

```bash
# Ativar virtualenv
eval $(poetry env activate)

# Instalar dependências
poetry install

# Rodar API
uvicorn api.main:app --reload --port 8000

# Docs interativos
open http://localhost:8000/docs
```

## Princípios arquiteturais

1. **Event-driven** — Gold emite eventos, workflows reagem (não polling)
2. **Delta perception** — LLM recebe *o que mudou*, não snapshot estático
3. **Human-in-the-loop** — agente propõe, analista aprova
4. **Memória organizacional** — RAG + Knowledge Graph + Diagram Vault
5. **Gestão da qualidade transversal** — MASP/Kaizen/ISO cruzam todas as camadas
