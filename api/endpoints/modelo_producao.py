from api.client import client

def fetch_modelos_producao_api():
    itens = []
    for page_items in client.paginate("/v1/ProductionOrderTemplate"):
        for entry in page_items:
            d = entry.get("data", {}) if isinstance(entry, dict) else {}
            itens.append({
                "id_aloee": d.get("id"),
                "id_produto_aloee": d.get("productId"),
                "descricao": d.get("description"),
                "cliente": d.get("customer"),
                "quantidade": d.get("quantity"),
                "observacoes": d.get("observations")
            })
    return itens
