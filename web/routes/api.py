from fastapi import APIRouter
from core.models.stats import AppStats
from core.models.account import Account
from sqlmodel import Session, select
from core.db import engine
#from core.services.account_service import get_accounts

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

    with Session(engine) as session:
        session.add(account)
        session.commit()
        session.refresh(account)

    # Save the account to the database
    return {"message": "Account created", "account": account}

@router.get("/accounts")
async def get_accounts():
    with Session(engine) as session:
        statement = select(Account)
        results = session.exec(statement)
        return results.all()