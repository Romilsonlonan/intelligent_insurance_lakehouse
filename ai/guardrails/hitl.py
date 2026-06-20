"""
Human-in-the-Loop (HITL) — guardrail central da arquitetura.

O agente PROPÕE, o analista APROVA. Nenhuma ação concreta é executada
sem passar por aqui quando o evento exige aprovação.

Em produção, isso pode ser integrado com:
- Slack (webhook de aprovação)
- Email com link de confirmação
- Interface Dash com botão de aprovação
"""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class ApprovalRequest(dict):
    """Request de aprovação enviado ao analista."""
    pass


class HumanInTheLoop:
    """
    Implementação base de HITL.
    Em desenvolvimento: simula aprovação automática (modo sandbox).
    Em produção: integrar com canal de notificação (Slack/Email/Dash).
    """

    def __init__(self, auto_approve: bool = False, timeout_seconds: int = 300) -> None:
        self.auto_approve = auto_approve
        self.timeout_seconds = timeout_seconds
        self._pending: dict[str, asyncio.Future] = {}

    async def request_approval(
        self,
        action: dict[str, Any],
        event_id: str,
        reviewer: str = "system",
    ) -> bool:
        """
        Solicita aprovação humana para uma ação proposta pelo agente.
        Retorna True se aprovado, False se rejeitado ou timeout.
        """
        logger.info(
            "[HITL] Approval requested for event '%s' | action: %s",
            event_id, action.get("target_agent"),
        )

        if self.auto_approve:
            logger.warning("[HITL] AUTO-APPROVE mode — action approved without human review.")
            return True

        # Em produção: notificar via webhook/email e aguardar resposta
        # Aqui, simula timeout → rejeita por segurança
        logger.info(
            "[HITL] Waiting %ds for human approval on event '%s'...",
            self.timeout_seconds, event_id,
        )
        await asyncio.sleep(0)   # placeholder para integração real
        return False             # default seguro: rejeitar se não houver resposta

    def approve(self, event_id: str, approved_by: str) -> None:
        """Chamado pelo endpoint da API quando o analista clica em 'Aprovar'."""
        future = self._pending.get(event_id)
        if future and not future.done():
            future.set_result((True, approved_by, datetime.utcnow()))
            logger.info("[HITL] Event '%s' approved by '%s'", event_id, approved_by)

    def reject(self, event_id: str, rejected_by: str, reason: str = "") -> None:
        """Chamado pelo endpoint da API quando o analista clica em 'Rejeitar'."""
        future = self._pending.get(event_id)
        if future and not future.done():
            future.set_result((False, rejected_by, datetime.utcnow()))
            logger.info(
                "[HITL] Event '%s' rejected by '%s'. Reason: %s",
                event_id, rejected_by, reason,
            )
