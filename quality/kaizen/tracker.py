"""
Kaizen Tracker — registra eventos de melhoria contínua.
Cada Kaizen tem: título, problema identificado, ação tomada, resultado medido e ciclo PDCA.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field
import uuid


class KaizenStatus(str, Enum):
    PLAN  = "P — Planejar"
    DO    = "D — Executar"
    CHECK = "C — Verificar"
    ACT   = "A — Agir/Padronizar"
    DONE  = "Concluído"


class KaizenEvent(BaseModel):
    kaizen_id: str = Field(default_factory=lambda: f"KAI-{uuid.uuid4().hex[:6].upper()}")
    title: str
    problem: str
    root_cause: str | None = None           # preenchido após Ishikawa
    action_taken: str | None = None
    result_measured: str | None = None
    responsible: str | None = None
    status: KaizenStatus = KaizenStatus.PLAN
    triggered_by_event: str | None = None   # event_id que gerou este Kaizen
    created_at: datetime = Field(default_factory=datetime.utcnow)
    closed_at: datetime | None = None
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def advance_pdca(self) -> KaizenStatus:
        order = list(KaizenStatus)
        idx = order.index(self.status)
        if idx + 1 < len(order):
            self.status = order[idx + 1]
            if self.status == KaizenStatus.DONE:
                self.closed_at = datetime.utcnow()
        return self.status


class KaizenTracker:
    """Repositório em memória de Kaizen events (substituir por persistência)."""

    def __init__(self) -> None:
        self._events: dict[str, KaizenEvent] = {}

    def register(self, title: str, problem: str, **kwargs) -> KaizenEvent:
        event = KaizenEvent(title=title, problem=problem, **kwargs)
        self._events[event.kaizen_id] = event
        return event

    def get(self, kaizen_id: str) -> KaizenEvent | None:
        return self._events.get(kaizen_id)

    def list_open(self) -> list[KaizenEvent]:
        return [e for e in self._events.values() if e.status != KaizenStatus.DONE]

    def advance(self, kaizen_id: str) -> KaizenStatus:
        event = self._events[kaizen_id]
        return event.advance_pdca()
