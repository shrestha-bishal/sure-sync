import os
from config import DATA_PATH
from sqlmodel import SQLModel, create_engine

DB_PATH = os.path.join(DATA_PATH, "sure-sync.db")
SQLITE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(SQLITE_URL)

def init_db():
    directory = os.path.dirname(DB_PATH)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    SQLModel.metadata.create_all(engine)