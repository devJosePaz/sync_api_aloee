# api/endpoints/produto.py
from api.client import client

def fetch_produtos_api():
    """
    Retorna lista de dicionários com apenas os campos que vamos usar.
    """
    itens_agrupados = []
    for page_items in client.paginate("/v1/Product"):
        for entry in page_items:
            d = entry.get("data", {}) if isinstance(entry, dict) else {}
            deps = d.get("previousProductsDependency", []) or []
            itens_agrupados.append({
                "id_aloee": d.get("id"),
                "descricao": d.get("name"),
                "unidade": d.get("unit"),
                "dependencia_nome": ", ".join(x.get("previousProductName", "") for x in deps) if deps else None,
                "dependencia_id_aloee": ", ".join(x.get("previousProductId", "") for x in deps) if deps else None
            })
    return itens_agrupados
