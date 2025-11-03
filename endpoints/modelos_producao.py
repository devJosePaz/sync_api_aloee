from utils.api_client import get_data

def fetch_modelos_producao(page_number=1, page_size=500):
    resp = get_data("/v1/ProductionOrderTemplate", page_number, page_size)
    if not resp or "collection" not in resp or "items" not in resp["collection"]:
        return []

    modelos = []
    for item in resp["collection"]["items"]:
        data = item.get("data", {})
        modelos.append({
            "id": data.get("id"),
            "name": data.get("name"),
            "product_api_id": data.get("productId"),  # <-- aqui é o mesmo que IdProdAloee do Produto
            "quantidade": data.get("productionQuantity", 0)
        })
    return modelos
