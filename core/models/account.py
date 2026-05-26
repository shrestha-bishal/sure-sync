from sqlmodel import SQLModel, Field, Session, create_engine
from datetime import datetime
from typing import Optional

class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sure_account_id: str
    bank_name: str
    account_id: str
    account_name: str

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    bank_id: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)