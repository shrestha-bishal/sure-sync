import os
import time
from app.helpers.logger import log
from app.helpers.file import move, read_json, write_json
from config import consume_path, processed_dir, failed_dir, volume_consume_path, lookup_interval, api_url, api_key, data_path
from datetime import datetime
from parsers.parser import Parser
from clients.api_client import ApiClient
from models.transaction import Transaction
from models.stats import AppStats

# Api validations
if not api_url:
    raise ValueError("API_URL environment variable is not set")

if not api_key:
    raise ValueError("API_KEY environment variable is not set")

log("App started")
log("API config validated")

# Create dir if does not exist
os.makedirs(consume_path, exist_ok=True)
os.makedirs(processed_dir, exist_ok=True)
os.makedirs(failed_dir, exist_ok=True)

log(f"Consume directory   : {volume_consume_path}")
log(f"Processed directory : {volume_consume_path}/processed")
log(f"Failed directory    : {volume_consume_path}/failed")
log(f"Scan interval       : {lookup_interval}s")

parser = Parser()
api_client = ApiClient(base_url=api_url, api_key=api_key)

# Fetching Sure account information
log("Fetching Sure account information")
sure_accounts = api_client.get_accounts()
sure_account_ids = {a['id'] for a in sure_accounts}
log(f"Found {len(sure_accounts)} Sure accounts")

# Retrieve the mapped accounts
log("Retrieving mapped accounts")
account_mappings = parser.parse("/app/data/account-mapping.yml")
log(f"Found {len(account_mappings)} account mappings")

# Validate mappings
log("Validating account mappings against Sure accounts")
valid_mappings = {}
invalid_mappings = []
for ofx_key, mapping in account_mappings.items():
    sure_id = mapping.get("sure_account_id")
    if sure_id in sure_account_ids:
        valid_mappings[ofx_key] = mapping

    else:    
        log(f"Mapping for '{ofx_key} points to non-existent Sure account ID '{sure_id}''")
        invalid_mappings.append(ofx_key)

log(f"{len(valid_mappings)} valid account mappings will be used")
if invalid_mappings:
    log(f"{len(invalid_mappings)} account mapping(s) are invalid and will be skipped")

stats = AppStats.load(os.path.join(data_path, "stats.json"), valid_mappings)
stats.save(os.path.join(data_path, "stats.json"))

# Consuming
while True:
    if not os.path.exists(consume_path):
        log(f"Consume path does not exist: {consume_path}")
        time.sleep(lookup_interval)
        continue

    for file_name in os.listdir(consume_path):
        file_path = os.path.join(consume_path, file_name)
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
                
                sure_account_id = mapping.get("sure_account_id")
                transaction = Transaction.from_ofx_data(
                    sure_account_id=sure_account_id,
                    data=data)

                api_client.create_transaction(transaction=transaction) 

            move(file_path, os.path.join(processed_dir, new_file_name))
            stats.on_success(file_name, os.path.join(data_path, "stats.json"))

        except ValueError as e:
            log(f"Unsupported file {file_name}: {e}")
            move(file_path, os.path.join(failed_dir, new_file_name))
            stats.on_failure(file_name, e, os.path.join(data_path, "stats.json"))

        except Exception as e:
            log(f"Error processing {file_name}: {e}")
            move(file_path, os.path.join(failed_dir, new_file_name))
            stats.on_failure(file_name, e, os.path.join(data_path, "stats.json"))

    time.sleep(lookup_interval)