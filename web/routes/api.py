from fastapi import APIRouter
from app.models.stats import AppStats

router = APIRouter(prefix="/api")

STATS_PATH = "/app/data/stats.json"

@router.get('/stats')
async def stats():
    return AppStats.load(STATS_PATH)