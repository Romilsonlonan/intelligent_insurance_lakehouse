"""
Schemas de eventos — contratos tipados para o Event Bus.
Cada evento carrega o delta (o que mudou) em relação ao estado anterior do Gold.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class EventType(str, Enum):
    NOVO_CENARIO          = "novo_cenario_cliente"
    KPI_FORA_LIMITE       = "kpi_fora_do_limite"
    NC_FECHADA            = "nc_fechada"
    DESVIO_DETECTADO      = "desvio_detectado"
    KAIZEN_REGISTRADO     = "kaizen_registrado"
    MASP_ABERTO           = "masp_aberto"
    MASP_CONCLUIDO        = "masp_concluido"
    AUDITORIA_ISO         = "auditoria_iso_9001"


class GoldDelta(BaseModel):
    """Representa o que mudou entre o estado anterior e o atual do Gold."""
    metric: str
    previous_value: float | None = None
    current_value: float
    variation_pct: float | None = None
    context: dict[str, Any] = Field(default_factory=dict)


class QualityEvent(BaseModel):
    """Evento base publicado pelo Gold layer no Event Bus."""
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str                        # ex.: "gold/kpis_apolices.parquet"
    client_segment: str | None = None
    delta: GoldDelta | None = None     # O que mudou — contexto para a LLM
    metadata: dict[str, Any] = Field(default_factory=dict)
    requires_human_approval: bool = False
