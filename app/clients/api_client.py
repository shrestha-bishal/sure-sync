from clients.base_client import BaseClient
from clients.accounts_client import AccountsClient
from clients.transactions_client import TransactionsClient
from models.transaction import Transaction

class ApiClient(BaseClient):
    def __init__(self, base_url, api_key):
        super().__init__(base_url, api_key)
        self.accounts_client = AccountsClient(self)
        self.transaction_client = TransactionsClient(self)

    def get_accounts(self, params=None):
        return self.accounts_client.list()

    def create_transaction(self, transaction: Transaction):
        self.transaction_client.create(transaction)