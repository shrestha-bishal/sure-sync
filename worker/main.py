import os
import time
from worker.helpers.logger import log
from worker.helpers.file import move, read_json, write_json
from core.config import CONSUME_PATH, PROCESSED_DIR, FAILED_DIR, VOLUME_CONSUME_PATH, LOOKUP_INTERVAL, API_URL, API_KEY, DATA_PATH
from core.db import init_db
from core.services.transaction_service import truncate_transactions
from core.clients.api_client import ApiClient
from core.models.transaction import Transaction
from core.models.stats import AppStats
from core.services.account_service import get_accounts
from core.services.transaction_service import create_transaction
from datetime import datetime
from parsers.parser import Parser

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

log(f"Consume directory   : {VOLUME_CONSUME_PATH}")
log(f"Processed directory : {VOLUME_CONSUME_PATH}/processed")
log(f"Failed directory    : {VOLUME_CONSUME_PATH}/failed")
log(f"Scan interval       : {LOOKUP_INTERVAL}s")

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
    sure_id = mapping.sure_account_id
    key = f"{mapping.bank_id}:{mapping.account_id}"
    if sure_id in sure_account_ids:
        valid_mappings[key] = mapping

    else:
        log(f"Mapping for '{key} points to non-existent Sure account ID '{sure_id}''")
        invalid_mappings.append(key)

log(f"{len(valid_mappings)} valid account mappings will be used")
if invalid_mappings:
    log(f"{len(invalid_mappings)} account mapping(s) are invalid and will be skipped")

stats = AppStats.load(os.path.join(DATA_PATH, "stats.json"), valid_mappings)
stats.save(os.path.join(DATA_PATH, "stats.json"))

# Consuming
while True:
    if not os.path.exists(CONSUME_PATH):
        log(f"Consume path does not exist: {CONSUME_PATH}")
        time.sleep(LOOKUP_INTERVAL)
        continue

    for file_name in os.listdir(CONSUME_PATH):
        file_path = os.path.join(CONSUME_PATH, file_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_file_name = f"{timestamp} {file_name}"

        # Skip directories (processed/, failed/)
        if not os.path.isfile(file_path):
            continue

        # Processing the data
        try:
            parsed_data = parser.parse(file_path)
            log(f"Parsed data from {file_name}")
            log(f"{parsed_data}")

            for data in parsed_data:
                bank_id = data.get("bank_id")
                account_id = data.get("account_id")
                key = f"{bank_id}:{account_id}"
                mapping = valid_mappings.get(key)

                if not mapping:
                    log(f"Account {key} not mapped. Skipping.")
                    continue
                
                sure_account_id = mapping.sure_account_id

                transaction = Transaction.from_ofx_data(
                    sure_account_id=sure_account_id,
                    data=data)

                api_client.create_transaction(transaction=transaction)
                create_transaction(mapping.id, transaction)

            move(file_path, os.path.join(PROCESSED_DIR, new_file_name))
            stats.on_success(file_name, os.path.join(DATA_PATH, "stats.json"))

        except ValueError as e:
            log(f"Unsupported file {file_name}: {e}")
            move(file_path, os.path.join(FAILED_DIR, new_file_name))
            stats.on_failure(file_name, e, os.path.join(DATA_PATH, "stats.json"))

        except Exception as e:
            log(f"Error processing {file_name}: {e}")
            move(file_path, os.path.join(FAILED_DIR, new_file_name))
            stats.on_failure(file_name, e, os.path.join(DATA_PATH, "stats.json"))

    time.sleep(LOOKUP_INTERVAL)