from sqlmodel import SQLModel, Field, Session, create_engine

class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sure_account_id: str
    bank_name: str,
    account_name: str,
    notes: str | None = None