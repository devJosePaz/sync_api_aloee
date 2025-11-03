# utils/api_client.py
import requests
from config import API_USER, API_PASSWORD, API_BASE_URL

def get_token():
    """Gera o token de autenticação da API Aloee"""
    url = f"{API_BASE_URL}/v1/Login"
    payload = {"Email": API_USER, "Password": API_PASSWORD}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        token = data["collection"]["items"][0]["data"].get("token")
        if not token:
            print("Token não retornado pela API.")
        return token
    except requests.exceptions.RequestException as e:
        print(f"Erro ao gerar token: {e}")
        return None

def get_data(endpoint: str, page_number: int = 1, page_size: int = 500):
    """Busca dados genéricos de qualquer endpoint paginado"""
    token = get_token()
    if not token:
        print("Não foi possível obter token. Abortando.")
        return None

    url = f"{API_BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept-Language": "pt-BR",
        "Content-Type": "application/json"
    }
    params = {"pageNumber": page_number, "pageSize": page_size}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return None
