from fastapi import APIRouter
from core.models.stats import AppStats
from core.models.account import Account
from core.services.account_service import get_accounts as get_all_accounts, create_account

router = APIRouter(prefix="/api")

DATA_PATH = "/app/data"

@router.get('/stats')
async def stats():
    return AppStats.load(DATA_PATH + "/stats.json")

@router.post("/accounts")
async def create_accounts():
    account = Account(
        sure_account_id="123",
        bank_name="Test Bank",
        account_id="456",
        account_name="Test Account",
    )
    
    success = create_account(account)
    return {"account": account, "success": success}

@router.get("/accounts")
async def get_accounts():
    return get_all_accounts()