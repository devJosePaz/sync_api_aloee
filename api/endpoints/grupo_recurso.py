#api/endpoints/grupo_recurso.py
from api.client import client

def fetch_grupos_recurso_api():
    itens = []

    for page_items in client.paginate("/v1/ResourceGroup"):
        for entry in page_items:
            d = entry.get("data", {}) if isinstance(entry, dict) else {}

            itens.append({
                "id_aloee": d.get("id"),
                "descricao": d.get("name"),
                "restricao": d.get("constraintType"),
                "unidade": d.get("unit"),
                "quantidade": d.get("quantity"),
                "maximo": d.get("maxPerResource"),
                "limites_oee": 'N' if d.get("usesDefaultAccountOee") else 'S',  # ou ajuste conforme regra
                "limite_a": d.get("oeeValueLimitA"),
                "limite_b": d.get("oeeValueLimitB"),
                "id_calendario_aloee": d.get("calendarId")
            })

    return itens
