import requests
from core.config import settings
from core.logger import log_info

class AloeeClient:
    def __init__(self):
        self.base = settings.ALOEE_URL.rstrip('/')
        self.user = settings.ALOEE_USER
        self.pwd = settings.ALOEE_PASS
        self._token = None

    def authenticate(self):
        if self._token:
            return self._token
        try:
            url = f"{self.base}/v1/Login"
            payload = {"Email": self.user, "Password": self.pwd}
            r = requests.post(url, json=payload, timeout=30)
            r.raise_for_status()
            data = r.json()
            token = None
            try:
                token = data["collection"]["items"][0]["data"].get("token")
            except Exception:
                token = data.get("token") or data.get("access_token")
            self._token = token
            return token
        except Exception as e:
            log_info(f"Falha ao autenticar na Aloee: {e}", "error")
            raise

    def _get_headers(self):
        token = self.authenticate()
        return {
            "Authorization": f"Bearer {token}" if token else "",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def get(self, path: str, params: dict = None):
        url = f"{self.base}{path}"
        try:
            r = requests.get(url, headers=self._get_headers(), params=params, timeout=60)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            log_info(f"GET {url} falhou: {e}", "error")
            raise

    def paginate(self, path: str, page_field="pageNumber", size_field="pageSize", page_start=1, page_size=None):
        if page_size is None:
            page_size = settings.PAGE_SIZE
        page = page_start
        while True:
            params = {page_field: page, size_field: page_size}
            data = self.get(path, params=params)
            if not data:
                break
            items = []
            if isinstance(data, dict) and "collection" in data and "items" in data["collection"]:
                items = data["collection"]["items"]
            elif isinstance(data, dict) and "items" in data:
                items = data["items"]
            elif isinstance(data, list):
                items = data
            else:
                break
            if not items:
                break
            yield items
            if isinstance(items, list) and len(items) < page_size:
                break
            page += 1

client = AloeeClient()
