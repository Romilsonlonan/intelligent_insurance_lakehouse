"""
Agent Memory — memória organizacional viva dos agentes.

Integra três camadas:
1. Short-term: buffer em memória (últimas N interações da sessão)
2. Long-term RAG: embeddings no vector store (histórico de eventos e decisões)
3. Knowledge Graph: relações causais persistidas (Neo4j)

A LLM recebe contexto histórico ANTES de agir — não apenas dados estáticos.
"""
from __future__ import annotations

import logging
from collections import deque
from datetime import datetime
from typing import Any

from events.schemas import QualityEvent

logger = logging.getLogger(__name__)


class AgentMemory:
    """
    Camada de memória híbrida: short-term (deque) + long-term (RAG/Graph).
    As integrações com vector store e Neo4j são injetadas via construtor
    para facilitar testes e troca de implementação.
    """

    def __init__(
        self,
        short_term_size: int = 20,
        rag_indexer=None,       # ai.rag.indexer.RAGIndexer (injetado)
        graph_connector=None,   # knowledge.graph.connector.GraphConnector (injetado)
    ) -> None:
        self._short_term: deque[dict[str, Any]] = deque(maxlen=short_term_size)
        self._rag = rag_indexer
        self._graph = graph_connector

    async def retrieve_relevant(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        """
        Busca contexto histórico relevante para a query.
        Combina short-term (recência) + RAG (semântica).
        """
        results: list[dict[str, Any]] = []

        # Short-term: itens mais recentes relacionados
        recent = [
            item for item in reversed(self._short_term)
            if query[:20].lower() in str(item).lower()
        ][:limit]
        results.extend(recent)

        # RAG (long-term semântico)
        if self._rag:
            try:
                rag_results = await self._rag.search(query=query, top_k=limit)
                results.extend(rag_results)
            except Exception as exc:
                logger.warning("RAG retrieval failed: %s", exc)

        # Knowledge Graph (relações causais)
        if self._graph:
            try:
                graph_results = await self._graph.query_related(query=query, limit=limit)
                results.extend(graph_results)
            except Exception as exc:
                logger.warning("Graph query failed: %s", exc)

        logger.info("Memory retrieved %d context items for query: '%s'", len(results), query[:50])
        return results[:limit]

    async def store(self, event: QualityEvent, response: dict[str, Any]) -> None:
        """Persiste evento + resposta do agente na memória."""
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_id": event.event_id,
            "event_type": event.event_type,
            "client_segment": event.client_segment,
            "delta": event.delta.model_dump() if event.delta else None,
            "agent_response": response,
        }
        # Short-term (imediato)
        self._short_term.append(record)

        # Long-term: indexar no RAG
        if self._rag:
            try:
                text = (
                    f"Evento {event.event_type} em {event.client_segment}. "
                    f"Delta: {event.delta}. Resposta: {response.get('target_agent')}"
                )
                await self._rag.index(doc_id=event.event_id, text=text, metadata=record)
            except Exception as exc:
                logger.warning("RAG indexing failed: %s", exc)

        logger.info("Memory stored event '%s'", event.event_id)
