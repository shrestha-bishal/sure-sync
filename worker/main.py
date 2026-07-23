import os
import time
from watchdog.observers.polling import PollingObserver as Observer
from handlers.ofx_handler import OFXHandler
from core.helpers.logger import log
from core.config import CONSUME_PATH, PROCESSED_DIR, FAILED_DIR, API_URL, API_KEY, DATA_PATH
from core.db import init_db
from core.services.transaction_service import truncate_transactions
from core.clients.api_client import ApiClient
from core.models.stats import AppStats
from core.services.account_service import get_accounts
from processors.ofx_processor import OFXProcessor
from parsers.parser import Parser
from datetime import datetime

# Api validations
if not API_URL:
    raise ValueError("API_URL environment variable is not set")

if not API_KEY:
    raise ValueError("API_KEY environment variable is not set")

log("App started")
log("API config validated")

# Create dir if does not exist
os.makedirs(CONSUME_PATH, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(FAILED_DIR, exist_ok=True)

log(f"Consume directory   : {CONSUME_PATH}")
log(f"Processed directory : {CONSUME_PATH}/processed")
log(f"Failed directory    : {CONSUME_PATH}/failed")

parser = Parser()
api_client = ApiClient(base_url=API_URL, api_key=API_KEY)

truncate_transactions()
init_db()

# Fetching Sure account information
log("Fetching Sure account information")
sure_accounts = api_client.get_accounts()
sure_account_ids = {a['id'] for a in sure_accounts}
log(f"Found {len(sure_accounts)} Sure accounts")

# Retrieve the mapped accounts
log("Retrieving mapped accounts")
account_mappings = get_accounts()
log(f"Found {len(account_mappings)} account mappings")

# Validate mappings
log("Validating account mappings against Sure accounts")

valid_mappings = {}
invalid_mappings = []

for mapping in account_mappings:
    key = f"{mapping.bank_id}:{mapping.account_id}"

    if mapping.sure_account_id in sure_account_ids:
        valid_mappings[key] = mapping

    else:
        log(f"Mapping for '{key} points to non-existent Sure account ID '{sure_id}''")
        invalid_mappings.append(key)

log(f"{len(valid_mappings)} valid account mappings will be used")

if invalid_mappings:
    log(f"{len(invalid_mappings)} account mapping(s) are invalid and will be skipped")

stats = AppStats.load(os.path.join(DATA_PATH, "stats.json"), valid_mappings)
stats.save(os.path.join(DATA_PATH, "stats.json"))

# ofx processor
processor = OFXProcessor(
    parser=parser,
    api_client=api_client,
    valid_mappings=valid_mappings,
    stats=stats
)

# Watcher
handler = OFXHandler(
    processor.process
)

# Process files already waiting
handler.process_existing_files(CONSUME_PATH)

observer = Observer()

observer.schedule(
    handler,
    CONSUME_PATH,
    recursive=False
)

observer.start()

log(f"Watching directory: {CONSUME_PATH}")


try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    observer.stop()

observer.join()