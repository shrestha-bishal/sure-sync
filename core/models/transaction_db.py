from sqlmodel import SQLModel, Field, Session, create_engine
from datetime import datetime
from typing import Optional

class Transaction(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        account_id: int
        date: str
        description: str
        amount: float
        currency: str
        nature: str
        is_successful: bool = Field(default=True)
        is_duplicate: bool = Field(default=False)
        message: Optional[str] = Field(default=None)