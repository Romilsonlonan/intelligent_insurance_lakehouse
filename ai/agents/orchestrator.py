"""
Orchestrator Agent — coordena todos os agentes de IA.

Fluxo principal:
1. Recebe QualityEvent do Event Bus
2. Lê o delta (o que mudou no Gold) e busca histórico no Knowledge Graph
3. Decide qual agente especialista acionar (MASP, Quality, Strategy)
4. Respeita o Human-in-the-loop antes de executar ações concretas
5. Registra tudo no Workflow Log Store e atualiza o RAG index
"""
from __future__ import annotations

import logging
from typing import Any

from events.schemas import EventType, QualityEvent
from ai.agents.memory import AgentMemory
from ai.guardrails.hitl import HumanInTheLoop

logger = logging.getLogger(__name__)


class OrchestratorAgent:
    def __init__(
        self,
        memory: AgentMemory,
        hitl: HumanInTheLoop,
    ) -> None:
        self.memory = memory
        self.hitl = hitl

    async def handle_event(self, event: QualityEvent) -> dict[str, Any]:
        """Ponto de entrada principal — chamado pelo Event Bus subscriber."""
        logger.info("Orchestrator received event: %s [%s]", event.event_type, event.event_id)

        # 1. Constrói contexto de delta para a LLM
        delta_context = self._build_delta_context(event)

        # 2. Busca histórico relevante da memória organizacional
        history = await self.memory.retrieve_relevant(
            query=delta_context["summary"],
            limit=5,
        )

        # 3. Decide qual agente acionar com base no tipo de evento
        agent_response = await self._dispatch(event, delta_context, history)

        # 4. Human-in-the-loop se o evento exige aprovação
        if event.requires_human_approval:
            approved = await self.hitl.request_approval(
                action=agent_response,
                event_id=event.event_id,
            )
            if not approved:
                logger.warning("Action rejected by human reviewer: %s", event.event_id)
                return {"status": "rejected", "event_id": event.event_id}

        # 5. Persiste na memória organizacional
        await self.memory.store(event=event, response=agent_response)

        return {"status": "dispatched", "event_id": event.event_id, "response": agent_response}

    def _build_delta_context(self, event: QualityEvent) -> dict[str, Any]:
        """
        Constrói o contexto de delta para a LLM.
        A LLM não recebe 'aqui estão os dados' — ela recebe 'aqui está o que mudou'.
        """
        if event.delta is None:
            return {"summary": f"Evento {event.event_type} sem delta estruturado."}

        d = event.delta
        variation_str = (
            f" (variação: {d.variation_pct:+.1f}%)" if d.variation_pct is not None else ""
        )
        summary = (
            f"Métrica '{d.metric}' mudou de {d.previous_value} para "
            f"{d.current_value}{variation_str}. Segmento: {event.client_segment}."
        )
        return {"summary": summary, "metric": d.metric, "delta": d.model_dump()}

    async def _dispatch(
        self,
        event: QualityEvent,
        delta_context: dict[str, Any],
        history: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Despacha para o agente especialista correto."""
        routing: dict[EventType, str] = {
            EventType.NOVO_CENARIO:     "masp_agent",
            EventType.KPI_FORA_LIMITE:  "quality_agent",
            EventType.DESVIO_DETECTADO: "quality_agent",
            EventType.NC_FECHADA:       "strategy_planner",
            EventType.MASP_CONCLUIDO:   "strategy_planner",
        }
        target = routing.get(event.event_type, "quality_agent")
        logger.info("Dispatching event %s → %s", event.event_type, target)

        # Aqui serão instanciados e chamados os agentes especializados
        return {
            "target_agent": target,
            "delta_context": delta_context,
            "history_items": len(history),
            "event_type": event.event_type,
        }
