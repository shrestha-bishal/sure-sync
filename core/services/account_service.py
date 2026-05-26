from sqlmodel import Session, select
from core.db import engine
from core.models.account import Account

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