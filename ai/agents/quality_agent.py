"""
Quality Agent — diagnóstico de qualidade via RAG + Gemma.

Recebe um evento de qualidade, busca contexto histórico (NCs, Kaizens,
ciclos DMAIC anteriores) e gera análise + recomendação com o Gemma.
"""
from __future__ import annotations

import logging
from typing import Any

from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from api.config import get_llm
from events.schemas import QualityEvent

logger = logging.getLogger(__name__)

QUALITY_PROMPT = ChatPromptTemplate.from_messages([
    (
        "human",
        """Você é um especialista em Gestão da Qualidade (Lean Six Sigma, MASP, ISO 9001).
Analise o evento abaixo e o contexto histórico fornecido.

EVENTO:
{event_summary}

CONTEXTO HISTÓRICO (NCs, Kaizens, ciclos DMAIC anteriores):
{history}

Responda em português com:
1. **Diagnóstico**: O que está acontecendo e por quê (use raciocínio baseado em causa-raiz)
2. **Fase DMAIC recomendada**: Qual fase ativar e por quê
3. **Ação imediata**: O que fazer nas próximas 24h
4. **Estratégia**: Plano de médio prazo (PDCA / MASP)
5. **Risco**: O que pode piorar se não agir

Seja objetivo, baseie-se nos dados do contexto histórico.""",
    )
])


class QualityAgent:
    """Agente de qualidade que usa Gemma para diagnóstico contextualizado."""

    def __init__(self, memory=None) -> None:
        self.memory = memory
        self._llm = None   # lazy init (evita erro se GOOGLE_API_KEY não configurada)

    def _get_chain(self):
        if self._llm is None:
            self._llm = get_llm()
        return (
            RunnablePassthrough()
            | QUALITY_PROMPT
            | self._llm
            | StrOutputParser()
        )

    async def diagnose(
        self,
        event: QualityEvent,
        history: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Gera diagnóstico de qualidade para um evento.

        Args:
            event: QualityEvent emitido pelo Gold layer
            history: Contexto histórico da memória organizacional

        Returns:
            dict com 'analysis' (texto do Gemma) e metadados
        """
        # Monta resumo do evento (delta perception)
        if event.delta:
            d = event.delta
            event_summary = (
                f"Tipo: {event.event_type}\n"
                f"Segmento: {event.client_segment}\n"
                f"Métrica: {d.metric}\n"
                f"Valor anterior: {d.previous_value}\n"
                f"Valor atual: {d.current_value}\n"
                f"Variação: {d.variation_pct:+.1f}%" if d.variation_pct else ""
            )
        else:
            event_summary = f"Tipo: {event.event_type} | Fonte: {event.source}"

        # Formata histórico
        history_text = "Nenhum histórico disponível."
        if history:
            items = []
            for h in history[:5]:
                items.append(
                    f"- [{h.get('timestamp', '?')}] {h.get('event_type', '?')}: "
                    f"{h.get('delta', {})}"
                )
            history_text = "\n".join(items)

        logger.info("QualityAgent: running Gemma diagnosis for event %s", event.event_id)

        try:
            chain = self._get_chain()
            analysis = chain.invoke({
                "event_summary": event_summary,
                "history": history_text,
            })
        except Exception as exc:
            logger.error("Gemma diagnosis failed: %s", exc)
            analysis = f"[Erro na análise — verifique GOOGLE_API_KEY]: {exc}"

        return {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "model": "gemma",
            "analysis": analysis,
        }
