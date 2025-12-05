import requests
from core.config import settings
from core.logger import log_info

class AloeeClient:
    def __init__(self):
        self.base_url = settings.ALOEE_URL
        self._token = None

    def _login(self):
        url = f"{self.base_url}/v1/Login"
        payload = {"Email": settings.ALOEE_USER, "Password": settings.ALOEE_PASS}

        resp = requests.post(url, json=payload)
        resp.raise_for_status()

        token = resp.json()["collection"]["items"][0]["data"].get("token")
        self._token = token
        return token

    def _get_headers(self):
        if not self._token:
            self._login()

        return {
            "Authorization": f"Bearer {self._token}",
            "Accept-Language": "pt-BR",
            "Content-Type": "application/json"
        }

    def get(self, endpoint, page=1, size=500):
        url = f"{self.base_url}{endpoint}"
        params = {"pageNumber": page, "pageSize": size}

        resp = requests.get(url, headers=self._get_headers(), params=params)
        resp.raise_for_status()
        return resp.json()

client = AloeeClient()
