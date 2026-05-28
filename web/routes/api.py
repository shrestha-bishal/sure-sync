from fastapi import APIRouter
from core.models.stats import AppStats
from core.models.account import Account
from core.services.account_service import get_accounts as get_all_accounts, create_account, update_account, delete_account, get_account_by_id, get_account_sync as get_all_account_sync
from core.services.transaction_service import get_all_transactions
from datetime import datetime
from typing import Optional

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

@router.get("/transactions")
async def get_transactions(start_date: Optional[str] = None, end_date: Optional[str] = None):
    return get_all_transactions(start_date=start_date, end_date=end_date)

@router.get("/accounts-sync")
async def get_accounts_sync():
    return get_all_account_sync()