from helpers.logger import log
from models.transaction import Transaction

class TransactionsClient:
    def __init__(self, base_client):
        self.base = base_client

    def post(self, transaction: Transaction):
        payload = { "transaction": transaction.to_json() }
        response = self.base.post("/transactions", json=payload)
        return response.get("transaction", response)
