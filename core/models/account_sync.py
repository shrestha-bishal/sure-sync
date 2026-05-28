from sqlmodel import SQLModel, Field, Session, create_engine
from datetime import datetime

class AccountSync(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    account_id: int
    last_synced_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)