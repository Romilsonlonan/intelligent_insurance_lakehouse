"""
Publishers — chamados pelo pipeline ETL ao gravar no Gold.
Transformam mudanças de estado em QualityEvents tipados.
"""
from __future__ import annotations

from events.bus import bus
from events.schemas import EventType, GoldDelta, QualityEvent


async def publish_novo_cenario(client_segment: str, delta: GoldDelta) -> None:
    event = QualityEvent(
        event_type=EventType.NOVO_CENARIO,
        source="gold/perfil_risco.parquet",
        client_segment=client_segment,
        delta=delta,
        requires_human_approval=True,
    )
    await bus.publish(event)


async def publish_kpi_fora_limite(metric: str, current: float, limit: float) -> None:
    event = QualityEvent(
        event_type=EventType.KPI_FORA_LIMITE,
        source="gold/kpis_apolices.parquet",
        delta=GoldDelta(metric=metric, current_value=current, context={"limit": limit}),
        requires_human_approval=False,
    )
    await bus.publish(event)


async def publish_nc_fechada(nc_id: str, resolution: str) -> None:
    event = QualityEvent(
        event_type=EventType.NC_FECHADA,
        source="quality/iso9001",
        metadata={"nc_id": nc_id, "resolution": resolution},
    )
    await bus.publish(event)


async def publish_desvio_detectado(metric: str, delta: GoldDelta) -> None:
    event = QualityEvent(
        event_type=EventType.DESVIO_DETECTADO,
        source="gold/compliance_report.parquet",
        delta=delta,
    )
    await bus.publish(event)
