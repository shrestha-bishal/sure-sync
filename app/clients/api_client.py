from clients.base_client import BaseClient
from clients.accounts_client import AccountsClient

class ApiClient(BaseClient):
    def __init__(self, base_url, api_key):
        super().__init__(base_url, api_key)
        self.accounts_client = AccountsClient(self)

    def get_accounts(self, params=None):
        return self.accounts_client.list()