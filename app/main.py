import os
import time
from helpers.logger import log
from helpers.file import move
from parsers.parser import Parser
from clients.api_client import ApiClient

CONSUME_PATH = "/app/consume"
PROCESSED_DIR = os.path.join(CONSUME_PATH, "processed")
FAILED_DIR = os.path.join(CONSUME_PATH, "failed")
VOLUME_CONSUME_PATH = os.getenv("CONSUME_PATH", CONSUME_PATH)
LOOKUP_INTERVAL = int(os.getenv("LOOKUP_INTERVAL", "5")) # default 5 seconds
API_URL = os.getenv("API_URL", None)
API_KEY = os.getenv("API_KEY", None)

if not API_URL:
    raise ValueError("API_URL environment variable is not set")

if not API_KEY:
    raise ValueError("API_KEY environment variable is not set")

log("App started")
log("API config validated")

api_client = ApiClient(base_url=API_URL, api_key=API_KEY)

log("Fetching account information")
log(api_client.get_accounts())

os.makedirs(CONSUME_PATH, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(FAILED_DIR, exist_ok=True)

log(f"Consume directory   : {VOLUME_CONSUME_PATH}")
log(f"Processed directory : {VOLUME_CONSUME_PATH}/processed")
log(f"Failed directory    : {VOLUME_CONSUME_PATH}/failed")
log(f"Scan interval       : {LOOKUP_INTERVAL}s")

parser = Parser()

while True:
    if not os.path.exists(CONSUME_PATH):
        log(f"Consume path does not exist: {CONSUME_PATH}")
        time.sleep(LOOKUP_INTERVAL)
        continue

    for file_name in os.listdir(CONSUME_PATH):
        file_path = os.path.join(CONSUME_PATH, file_name)

        # Skip directories (processed/, failed/)
        if not os.path.isfile(file_path):
            continue

        try:
            parsed_data = parser.parse(file_path)
            log(f"{parsed_data}")
            log(f"Parsed data from {file_name}")
            move(file_path, PROCESSED_DIR)

        except ValueError as e:
            log(f"Unsupported file {file_name}: {e}")
            move(file_path, FAILED_DIR)
        
        except Exception as e:
            log(f"Error processing {file_name}: {e}")
            move(file_path, FAILED_DIR)

    time.sleep(LOOKUP_INTERVAL)
