"""
FastAPI — entry point da aplicação.

Startup:
1. Registra todos os handlers do Event Bus
2. Inicializa middlewares de autenticação (JWT+RBAC) e auditoria LGPD
3. Monta todos os routers por domínio de negócio
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from workflows.gold_event_handler import register_all_handlers
from api.routers import clientes, apolices, ai_agent, compliance, quality, events
from api.middleware.audit import AuditMiddleware

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup e shutdown da aplicação."""
    logger.info("🚀 Starting Prudential Lakehouse Intelligence API v2")
    register_all_handlers()
    logger.info("✅ Event Bus handlers registered")
    yield
    logger.info("🛑 Shutting down API")


app = FastAPI(
    title="Prudential Lakehouse Intelligence",
    description=(
        "API event-driven para Gestão da Qualidade — "
        "Lean Six Sigma · MASP · ISO 9001 · DMAIC · Kaizen · IA Contextualizada"
    ),
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── Middlewares ──────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restringir em produção
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuditMiddleware)

# ── Routers ──────────────────────────────────────────────────────────────────
app.include_router(clientes.router,   prefix="/clientes",   tags=["Clientes"])
app.include_router(apolices.router,   prefix="/apolices",   tags=["Apólices"])
app.include_router(quality.router,    prefix="/quality",    tags=["Qualidade"])
app.include_router(ai_agent.router,   prefix="/ai",         tags=["IA / Agentes"])
app.include_router(compliance.router, prefix="/compliance", tags=["Compliance"])
app.include_router(events.router,     prefix="/events",     tags=["Events / HITL"])


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    return {"status": "ok", "version": "2.0.0"}
