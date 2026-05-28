from sqlmodel import Session, select
from core.db import engine
from core.models.transaction_db import Transaction as TransactionDb
from core.models.transaction import Transaction

def create_transaction(account_id: int, transaction: Transaction) -> bool:
    with Session(engine) as session:
        transaction_db = TransactionDb(
            account_id=account_id,
            date=transaction.date,
            description=transaction.description,
            amount=float(transaction.amount),
            currency=transaction.currency,
            nature=transaction.nature,
            is_successful=True,
            is_duplicate=False,
            message=None,
        )
        session.add(transaction_db)
        session.commit()
        session.refresh(transaction_db)