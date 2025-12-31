from helpers.logger import log

class AccountsClient:
    def __init__(self, base_client):
        self.base = base_client

    def list(self, params=None):
        url = f"{self.base.base_url}/accounts"
        log(f"Sending GET request to {url} with params={params}")
        return self.base.get("/accounts", params=params)