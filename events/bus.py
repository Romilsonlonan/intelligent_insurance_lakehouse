"""
Event Bus — Sistema nervoso central da arquitetura event-driven.
Publica eventos do Gold layer e despacha para subscribers registrados.
"""
from __future__ import annotations

import asyncio
import logging
from collections import defaultdict
from typing import Callable, Awaitable

from events.schemas import QualityEvent

logger = logging.getLogger(__name__)

# Tipo de handler: recebe um QualityEvent, retorna coroutine
EventHandler = Callable[[QualityEvent], Awaitable[None]]


class EventBus:
    """Bus assíncrono em memória (pode ser substituído por Kafka/Redis Streams)."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """Registra um handler para um tipo de evento."""
        self._handlers[event_type].append(handler)
        logger.info("Subscribed handler %s to event '%s'", handler.__name__, event_type)

    async def publish(self, event: QualityEvent) -> None:
        """Publica um evento e dispara todos os handlers registrados."""
        handlers = self._handlers.get(event.event_type, [])
        if not handlers:
            logger.warning("No handlers for event '%s'", event.event_type)
            return

        logger.info(
            "Publishing event '%s' [id=%s] to %d handler(s)",
            event.event_type, event.event_id, len(handlers),
        )
        await asyncio.gather(*[h(event) for h in handlers], return_exceptions=True)


# Instância global (singleton)
bus = EventBus()
