"""
Gatilho DMAIC — mapeamento automático de eventos Gold → fase DMAIC.

Bronze = Medir  (dados brutos chegam)
Silver = Analisar (limpeza, enriquecimento com LLM)
Gold   = Melhorar / Controlar (KPIs, compliance, Pareto)

Quando um evento chega do Event Bus, este módulo determina qual fase
do DMAIC deve ser acionada e que workflow de qualidade deve ser iniciado.
"""
from __future__ import annotations

import logging
from enum import Enum

from events.schemas import EventType, QualityEvent

logger = logging.getLogger(__name__)


class DMAICPhase(str, Enum):
    DEFINIR    = "D — Definir"
    MEDIR      = "M — Medir"
    ANALISAR   = "A — Analisar"
    MELHORAR   = "I — Melhorar"
    CONTROLAR  = "C — Controlar"


# Mapeamento: tipo de evento → fase DMAIC recomendada
EVENT_TO_PHASE: dict[EventType, DMAICPhase] = {
    EventType.NOVO_CENARIO:       DMAICPhase.DEFINIR,
    EventType.DESVIO_DETECTADO:   DMAICPhase.MEDIR,
    EventType.KPI_FORA_LIMITE:    DMAICPhase.ANALISAR,
    EventType.NC_FECHADA:         DMAICPhase.MELHORAR,
    EventType.KAIZEN_REGISTRADO:  DMAICPhase.MELHORAR,
    EventType.MASP_CONCLUIDO:     DMAICPhase.CONTROLAR,
    EventType.AUDITORIA_ISO:      DMAICPhase.CONTROLAR,
}

# Fase → ação recomendada de workflow
PHASE_TO_WORKFLOW: dict[DMAICPhase, str] = {
    DMAICPhase.DEFINIR:   "open_masp",
    DMAICPhase.MEDIR:     "run_pareto_analysis",
    DMAICPhase.ANALISAR:  "run_ishikawa_builder",
    DMAICPhase.MELHORAR:  "register_kaizen",
    DMAICPhase.CONTROLAR: "update_control_chart",
}


class DMAICTrigger:
    """Avalia um QualityEvent e retorna fase + workflow recomendado."""

    def evaluate(self, event: QualityEvent) -> tuple[DMAICPhase, str]:
        phase = EVENT_TO_PHASE.get(event.event_type, DMAICPhase.MEDIR)
        workflow = PHASE_TO_WORKFLOW[phase]
        logger.info(
            "Event '%s' → DMAIC phase '%s' → workflow '%s'",
            event.event_type, phase, workflow,
        )
        return phase, workflow
