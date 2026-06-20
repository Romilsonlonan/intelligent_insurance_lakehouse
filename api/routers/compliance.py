from fastapi import APIRouter
router = APIRouter()

@router.get("/report")
async def compliance_report():
    return {"status": "ok", "nc_abertas": 0, "nc_fechadas": 0}
