from core.clients.base_client import BaseClient
from core.clients.accounts_client import AccountsClient
from core.clients.transactions_client import TransactionsClient
from core.models.transaction import Transaction
from core.models.creation_result import CreationResult

class ApiClient(BaseClient):
    def __init__(self, base_url, api_key):
        super().__init__(base_url, api_key)
        self.accounts_client = AccountsClient(self)
        self.transaction_client = TransactionsClient(self)

    def get_accounts(self, params=None):
        return self.accounts_client.list()
    
    def get_transactions(self, params=None):
        return self.transaction_client.list(params=params)
    
    def get_transactions_by_date(self, from_date, to_date, account_ids=None, transaction_type=None):
        return self.transaction_client.list_transactions_by_date(
            from_date=from_date,
            to_date=to_date,
            account_ids=account_ids,
            transaction_type=transaction_type
        )

    def create_transaction(self, transaction: Transaction) -> CreationResult:
        return self.transaction_client.create(transaction)