# api/endpoints/modelo_producao.py
from api.client import client

def fetch_modelos_api():
    """
    Retorna lista de dicts compatíveis com services/modelo_producao_service.py

    """
    itens = []
    for page_items in client.paginate("/v1/ProductionOrderTemplate"):
        for entry in page_items:
            d = entry.get("data", {}) if isinstance(entry, dict) else {}
            itens.append({
                "id_modelo_aloee": d.get("id"),
                "id_produto_aloee": d.get("productId") or (d.get("product") or {}).get("id"),
                "descricao": d.get("description") or d.get("name"),
                "cliente": d.get("customer") or d.get("client") or d.get("customerName"),
                "quantidade": d.get("quantity") if d.get("quantity") is not None else 0,
                "observacoes": d.get("observations") or d.get("notes")
            })
    return itens
