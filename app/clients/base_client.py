import requests

class BaseClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _headers(self):
        headers = { "Content-Type": "application/json" }
        if(self.api_key):
            headers["X-Api-Key"] = f"{self.api_key}"

        return headers
    
    def get(self, path, params=None):
        res = requests.get(
            f"{self.base_url}{path}",
            headers=self._headers(),
            params=params,
            timeout=10
        )

        res.raise_for_status()

        if not res.content:
            return None

        try:
            return res.json()
        except ValueError:
            return res.text