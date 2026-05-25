from fastapi import APIRouter
from worker.models.stats import AppStats

router = APIRouter(prefix="/api")

DATA_PATH = "/app/data"

@router.get('/stats')
async def stats():
    return AppStats.load(DATA_PATH + "/stats.json")