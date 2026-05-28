from sqlmodel import Session, select
from core.db import engine
from core.models.account import Account
from core.models.account_sync import AccountSync
from datetime import datetime

def create_account(account: Account) -> bool:
    with Session(engine) as session:
        session.add(account)
        session.commit()
        session.refresh(account)

    return account.id is not None

def get_account_by_id(account_id: int) -> Account:
    with Session(engine) as session:
        account = session.get(Account, account_id)
        return account

def get_accounts():
    with Session(engine) as session:
        statement = select(Account)
        results = session.exec(statement)
        return results.all()

def update_account(account_id: int, updated_data: Account) -> bool:
    with Session(engine) as session:
        account = get_account_by_id(account_id)
        if not account:
            return False
        
        account_data = updated_data.model_dump(exclude_unset=True)
        for key, value in account_data.items():
            setattr(account, key, value)

        session.add(account)
        session.commit()
        session.refresh(account)
        return True

def delete_account(account_id: int) -> bool:
    with Session(engine) as session:
        account = get_account_by_id(account_id)
        if not account:
            return False
        
        session.delete(account)
        session.commit()
        return True

def upsert_account_sync(account_id: int):
    with Session(engine) as session:
        statement = select(AccountSync).where(AccountSync.account_id == account_id)
        account_sync = session.execute(statement).scalar_one_or_none()

        if not account_sync:
            account_sync = AccountSync(account_id=account_id)

        account_sync.last_synced_at = datetime.utcnow()
        session.add(account_sync)
        session.commit()
        session.refresh(account_sync)

        return account_sync

def get_account_sync():
    with Session(engine) as session:
        statement = select(AccountSync)
        results = session.exec(statement)
        return results.all()