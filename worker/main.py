import os
import time
from watchdog.observers.polling import PollingObserver as Observer
from handlers.ofx_handler import OFXHandler
from core.helpers.logger import log
from core.helpers.file import move, archive_file
from core.config import CONSUME_PATH, PROCESSED_DIR, FAILED_DIR, API_URL, API_KEY, DATA_PATH
from core.db import init_db
from core.services.transaction_service import truncate_transactions
from core.clients.api_client import ApiClient
from core.models.transaction import Transaction
from core.models.stats import AppStats
from core.services.account_service import get_accounts, upsert_account_sync
from core.services.transaction_service import create_transaction
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

# Consuming
def process_file(file_path):
    file_name = os.path.basename(file_path)
    log(f"Processing file: {file_name}") 

    account_name = None
    bank_name = None 

    # Processing the data
    try:
        parsed_data = parser.parse(file_path)
        log(f"Parsed data from {file_name}")

        if not parsed_data:
            raise ValueError("No transactions found")

        mapped_transactions = []

        for data in parsed_data:
            bank_id = data.get("bank_id")
            account_id = data.get("account_id")

            key = f"{bank_id}:{account_id}"
            mapping = valid_mappings.get(key)

            if not mapping:
                log(f"Account {key} not mapped. Skipping.")
                raise ValueError(f"Account {key} is not mapped")


            mapped_transactions.append({
                "data": data,
                "mapping": mapping
            })

        transaction_dates = [
            item["data"].get("date")
            for item in mapped_transactions
        ]

        from_date = min(transaction_dates)
        to_date = max(transaction_dates)

        sure_account_ids = list({
            item["mapping"].sure_account_id
            for item in mapped_transactions
        })

        existing_transactions = api_client.get_transactions_by_date(
            from_date=from_date,
            to_date=to_date,
            account_ids=list(sure_account_ids)
        )

        log(existing_transactions)

        for item in mapped_transactions:
            data = item["data"]
            mapping = item["mapping"]

            account_name = mapping.account_name
            bank_name = mapping.bank_name

            transaction = Transaction.from_ofx_data(
                sure_account_id=mapping.sure_account_id,
                data=data)

            result = api_client.create_transaction(transaction=transaction)
            create_transaction(mapping.id, transaction, result)
            upsert_account_sync(mapping.id) 

        move(
            file_path,
            archive_file(
                PROCESSED_DIR,
                bank_name,
                account_name,
                file_name,
                from_date,
                to_date
            )
        )

        stats.on_success(file_name, os.path.join(DATA_PATH, "stats.json"))

    except ValueError as e:
        log(f"Unsupported file {file_name}: {e}")
        move(
            file_path,
            archive_file(
                FAILED_DIR,
                bank_name,
                account_name,
                file_name
            )
        )

        stats.on_failure(file_name, e, os.path.join(DATA_PATH, "stats.json"))

    except Exception as e:
        log(f"Error processing {file_name}: {e}")
        move(
            file_path,
            archive_file(
                FAILED_DIR,
                bank_name,
                account_name,
                file_name
            )
        )

        stats.on_failure(file_name, e, os.path.join(DATA_PATH, "stats.json"))

# Watcher
handler = OFXHandler(
    process_file
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