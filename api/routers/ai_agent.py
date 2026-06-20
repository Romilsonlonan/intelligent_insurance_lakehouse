"""Routers placeholder — serão expandidos por domínio."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_ai_status():
    return {"agents": ["orchestrator", "masp_agent", "quality_agent", "strategy_planner"]}


@router.post("/query")
async def query_agent(question: str, segment: str | None = None):
    """Envia uma pergunta para o Quality Agent via RAG."""
    return {"answer": "Em implementação", "question": question, "segment": segment}
