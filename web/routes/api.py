from fastapi import APIRouter
from core.models.stats import AppStats
from core.models.account import Account
from core.services.account_service import get_accounts as get_all_accounts, create_account, update_account, delete_account, get_account_by_id

router = APIRouter(prefix="/api")

DATA_PATH = "/app/data"

@router.get('/stats')
async def stats():
    return AppStats.load(DATA_PATH + "/stats.json")

@router.post("/accounts")
async def create_accounts(account: Account):
    success = create_account(account)
    return {"account": account, "success": success}

@router.get("/accounts")
async def get_accounts():
    return get_all_accounts()

@router.get("/accounts/{account_id}")
async def get_account(account_id: int):
    account = get_account_by_id(account_id)
    if account:
        return account
    return {"error": "Account not found"}

@router.put("/accounts/{account_id}")
async def edit_account(account_id: int, account: Account):
    success = update_account(account_id, account)
    return {"success": success}

@router.delete("/accounts/{account_id}")
async def remove_account(account_id: int):
    success = delete_account(account_id)
    return {"success": success}