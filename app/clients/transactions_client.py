from helpers.logger import log
from models.transaction import Transaction

class TransactionsClient:
    def __init__(self, base_client):
        self.base = base_client

    def list(self, params=None):
        return self.base.get("/transactions", params=params)

    def exists(self, transaction: Transaction) -> bool:
        params = {
            "account_id": transaction.account_id,
            "date": transaction.date,
            "amount": transaction.amount,
            "currency": transaction.currency,
        }

        response = self.list(params=params)

        for existing in response.get("transactions", []):
            if existing.get("name") == transaction.name:
                return True

        return False
    
    def create(self, transaction: Transaction):
        if self.exists(transaction):
            log(
                f"[DUPLICATE] Transaction skipped | "
                f"Account: {transaction.account_id} | "
                f"Date: {transaction.date} | "
                f"Amount: {transaction.amount:.2f} {transaction.currency} | "
                f"Name: {transaction.name} | "
                f"Nature: {transaction.nature}"
            )

            return None

        payload = { "transaction": transaction.to_json() }

        log(
            f"[CREATE] Creating transaction | "
            f"Account: {transaction.account_id} | "
            f"Date: {transaction.date} | "
            f"Amount: {transaction.amount:.2f} {transaction.currency} | "
            f"Name: {transaction.name} | "
            f"Nature: {transaction.nature}"
        )

        response = self.base.post("/transactions", json=payload)

        log(f"Transaction created: {response}")
        return response.get("transaction", response)
