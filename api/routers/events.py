"""Router de Eventos / HITL — aprovação e rejeição humana de ações de IA."""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ApprovalPayload(BaseModel):
    approved_by: str
    reason: str = ""


@router.get("/pending")
async def list_pending_approvals():
    """Lista aprovações pendentes de revisão humana."""
    return {"pending": []}


@router.post("/{event_id}/approve")
async def approve_action(event_id: str, payload: ApprovalPayload):
    """Aprova uma ação proposta pelo agente."""
    return {"event_id": event_id, "status": "approved", "approved_by": payload.approved_by}


@router.post("/{event_id}/reject")
async def reject_action(event_id: str, payload: ApprovalPayload):
    """Rejeita uma ação proposta pelo agente."""
    return {"event_id": event_id, "status": "rejected", "rejected_by": payload.approved_by, "reason": payload.reason}
