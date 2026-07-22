import os

CONSUME_PATH = os.getenv("CONSUME_PATH", "/app/consume")
PROCESSED_DIR = os.path.join(CONSUME_PATH, "processed")
FAILED_DIR = os.path.join(CONSUME_PATH, "failed")

API_URL = os.getenv("API_URL", None)
API_KEY = os.getenv("API_KEY", None)

DATA_PATH = os.getenv("DATA_PATH", "/app/data")