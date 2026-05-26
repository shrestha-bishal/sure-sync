from sqlmodel import Session, select
from core.db import engine
from core.models.account import Account

def create_account(account: Account) -> bool:
    with Session(engine) as session:
        session.add(account)
        session.commit()
        session.refresh(account)

    return account.id is not None

def get_accounts():
    with Session(engine) as session:
        statement = select(Account)
        results = session.exec(statement)
        return results.all()