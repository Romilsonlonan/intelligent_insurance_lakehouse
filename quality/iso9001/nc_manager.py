"""
ISO 9001 NC Manager — gerencia Não-Conformidades com prazo e ação corretiva.
Cada NC segue o ciclo: Detecção → Análise → Ação Corretiva → Verificação → Encerramento.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field
import uuid


class NCStatus(str, Enum):
    ABERTA           = "aberta"
    EM_ANALISE       = "em_analise"
    ACAO_CORRETIVA   = "acao_corretiva"
    VERIFICACAO      = "verificacao"
    ENCERRADA        = "encerrada"
    REABERTA         = "reaberta"


class NonConformity(BaseModel):
    nc_id: str = Field(default_factory=lambda: f"NC-{uuid.uuid4().hex[:6].upper()}")
    title: str
    description: str
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    detected_by: str | None = None
    iso_clause: str | None = None           # ex.: "8.7 — Controle de saídas não conformes"
    status: NCStatus = NCStatus.ABERTA
    root_cause: str | None = None
    corrective_action: str | None = None
    responsible: str | None = None
    due_date: datetime | None = None
    closed_at: datetime | None = None
    verified_by: str | None = None
    triggered_masp: str | None = None       # masp_id se um MASP foi aberto para esta NC
    triggered_by_event: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def is_overdue(self) -> bool:
        if self.due_date and self.status not in (NCStatus.ENCERRADA,):
            return datetime.utcnow() > self.due_date
        return False

    def close(self, verified_by: str, resolution: str) -> None:
        self.status = NCStatus.ENCERRADA
        self.closed_at = datetime.utcnow()
        self.verified_by = verified_by
        self.corrective_action = resolution


class NCManager:
    """Repositório em memória de NCs (substituir por banco persistente)."""

    def __init__(self) -> None:
        self._ncs: dict[str, NonConformity] = {}

    def open_nc(
        self,
        title: str,
        description: str,
        iso_clause: str | None = None,
        days_to_resolve: int = 30,
        **kwargs,
    ) -> NonConformity:
        nc = NonConformity(
            title=title,
            description=description,
            iso_clause=iso_clause,
            due_date=datetime.utcnow() + timedelta(days=days_to_resolve),
            **kwargs,
        )
        self._ncs[nc.nc_id] = nc
        return nc

    def get(self, nc_id: str) -> NonConformity | None:
        return self._ncs.get(nc_id)

    def list_open(self) -> list[NonConformity]:
        return [nc for nc in self._ncs.values() if nc.status != NCStatus.ENCERRADA]

    def list_overdue(self) -> list[NonConformity]:
        return [nc for nc in self.list_open() if nc.is_overdue]

    def close(self, nc_id: str, verified_by: str, resolution: str) -> NonConformity:
        nc = self._ncs[nc_id]
        nc.close(verified_by=verified_by, resolution=resolution)
        return nc
