from helpers.logger import log
from models.transaction import Transaction

class TransactionsClient:
    def __init__(self, base_client):
        self.base = base_client

    def create(self, transaction: Transaction):
        payload = { "transaction": transaction.to_json() }

        log(
            f"Creating transaction for account {transaction.account_id} | "
            f"Date: {transaction.date} | Amount: {transaction.amount} | "
            f"Name: {transaction.name} | Nature: {transaction.nature}"
        )

        response = self.base.post("/transactions", json=payload)

        log(f"Transaction created: {response}")
        return response.get("transaction", response)
