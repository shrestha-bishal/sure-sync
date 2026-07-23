import os
from core.helpers.logger import log
from core.services.transaction_service import create_transaction
from core.services.account_service import upsert_account_sync
from core.models.transaction import Transaction
from core.helpers.file import move, archive_file
from core.config import PROCESSED_DIR, FAILED_DIR, DATA_PATH

class OFXProcessor:
    def __init__(
        self,
        parser,
        api_client,
        valid_mappings,
        stats
    ):
        self.parser = parser
        self.api_client = api_client
        self.valid_mappings = valid_mappings
        self.stats = stats

    def process(self, file_path):
        file_name = os.path.basename(file_path)
        log(f"Processing file: {file_name}") 

        account_name = None
        bank_name = None 

        # Processing the data
        try:
            parsed_data = self.parser.parse(file_path)
            log(f"Parsed data from {file_name}")

            if not parsed_data:
                raise ValueError("No transactions found")

            mapped_transactions = []

            for data in parsed_data:
                bank_id = data.get("bank_id")
                account_id = data.get("account_id")

                key = f"{bank_id}:{account_id}"
                mapping = self.valid_mappings.get(key)

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

            existing_transactions = self.api_client.get_transactions_by_date(
                from_date=from_date,
                to_date=to_date,
                account_ids=list(sure_account_ids)
            )

            for item in mapped_transactions:
                data = item["data"]
                mapping = item["mapping"]

                account_name = mapping.account_name
                bank_name = mapping.bank_name

                transaction = Transaction.from_ofx_data(
                    sure_account_id=mapping.sure_account_id,
                    data=data)

                result = self.api_client.create_transaction(transaction=transaction)
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

            self.stats.on_success(file_name, os.path.join(DATA_PATH, "stats.json"))

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

            self.stats.on_failure(file_name, e, os.path.join(DATA_PATH, "stats.json"))

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

            self.stats.on_failure(file_name, e, os.path.join(DATA_PATH, "stats.json"))