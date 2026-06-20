"""
Gold Event Handler — subscriber principal do Event Bus.

Registra handlers para todos os eventos emitidos pelo Gold layer.
É aqui que o ciclo event-driven começa: Gold publica → este handler reage.
"""
from __future__ import annotations

import logging

from events.bus import bus
from events.schemas import EventType, QualityEvent
from quality.dmaic.trigger import DMAICTrigger
from quality.masp.state_machine import MASPProcess, MASPStep, StepStatus

logger = logging.getLogger(__name__)

dmaic_trigger = DMAICTrigger()

# Repositório em memória (substituir por banco persistente)
_masp_registry: dict[str, MASPProcess] = {}


async def on_novo_cenario(event: QualityEvent) -> None:
    """Novo perfil de risco criado no Gold → abre MASP automaticamente."""
    phase, workflow = dmaic_trigger.evaluate(event)
    logger.info("NOVO CENÁRIO → fase %s → %s", phase, workflow)

    masp = MASPProcess(
        masp_id=f"MASP-{event.event_id[:8].upper()}",
        title=f"Análise de novo cenário: {event.client_segment}",
        triggered_by_event=event.event_id,
    )
    masp.steps[MASPStep.S1_IDENTIFICACAO].status = StepStatus.EM_ANDAMENTO
    _masp_registry[masp.masp_id] = masp
    logger.info("MASP aberto: %s | Progresso: %.1f%%", masp.masp_id, masp.progress_pct)


async def on_kpi_fora_limite(event: QualityEvent) -> None:
    """KPI violado → aciona análise de Pareto + Ishikawa."""
    phase, workflow = dmaic_trigger.evaluate(event)
    logger.info(
        "KPI FORA DO LIMITE → métrica: %s | valor: %s | fase: %s → %s",
        event.delta.metric if event.delta else "N/A",
        event.delta.current_value if event.delta else "N/A",
        phase, workflow,
    )
    # TODO: disparar análise automática de Pareto via quality.tools.pareto


async def on_nc_fechada(event: QualityEvent) -> None:
    """NC fechada → registrar melhoria e acionar loop Kaizen."""
    phase, workflow = dmaic_trigger.evaluate(event)
    nc_id = event.metadata.get("nc_id", "N/A")
    resolution = event.metadata.get("resolution", "N/A")
    logger.info(
        "NC FECHADA → nc_id: %s | resolução: %s | fase: %s → %s",
        nc_id, resolution, phase, workflow,
    )
    # TODO: registrar Kaizen event + atualizar Knowledge Graph


async def on_desvio_detectado(event: QualityEvent) -> None:
    """Desvio detectado → IA analisa delta histórico e propõe ação."""
    phase, workflow = dmaic_trigger.evaluate(event)
    logger.info("DESVIO DETECTADO → fase %s → %s", phase, workflow)
    # TODO: chamar OrchestratorAgent com contexto de delta


def register_all_handlers() -> None:
    """Registra todos os handlers no Event Bus. Chamar no startup da aplicação."""
    bus.subscribe(EventType.NOVO_CENARIO,     on_novo_cenario)
    bus.subscribe(EventType.KPI_FORA_LIMITE,  on_kpi_fora_limite)
    bus.subscribe(EventType.NC_FECHADA,       on_nc_fechada)
    bus.subscribe(EventType.DESVIO_DETECTADO, on_desvio_detectado)
    logger.info("All Gold event handlers registered.")
