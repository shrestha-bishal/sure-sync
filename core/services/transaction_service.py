from sqlmodel import Session, select, delete
from core.db import engine
from core.models.transaction_db import Transaction as TransactionDb
from core.models.creation_result import CreationResult
from core.models.transaction import Transaction
from typing import Optional

def create_transaction(account_id: int, transaction: Transaction, result: CreationResult) -> bool:
    with Session(engine) as session:
        transaction_db = TransactionDb(
            account_id=account_id,
            date=transaction.date,
            description=transaction.description,
            amount=float(transaction.amount),
            currency=transaction.currency,
            nature=transaction.nature,
            is_successful=result.is_successful,
            is_duplicate=result.is_duplicate,
            message=result.message,
        )
        session.add(transaction_db)
        session.commit()
        session.refresh(transaction_db)

def truncate_transactions():
    with Session(engine) as session:
        statement = delete(TransactionDb)
        session.exec(statement)
        session.commit()

def get_all_transactions(start_date: Optional[str] = None, end_date: Optional[str] = None):
    with Session(engine) as session:
        statement = select(TransactionDb)
        if start_date:
            statement = statement.where(TransactionDb.created_at >= start_date)
        if end_date:
            statement = statement.where(TransactionDb.created_at <= end_date)
            
        statement = statement.order_by(TransactionDb.date.asc())
        
        results = session.exec(statement)
        return results.all()
    