from fastapi import APIRouter

from app.metrics import get_system_metrics


router = APIRouter(prefix="/metrics", tags=["System Metrics"])


@router.get("/system")
def read_system_metrics():
    return get_system_metrics()