from utils.api_client import get_data

def fetch_produtos(page_number=1, page_size=500):
    resp = get_data("/v1/Product", page_number, page_size) # resposta da requisição 
    if not resp or "collection" not in resp or "items" not in resp["collection"]:
        return []

    produtos = []
    for item in resp["collection"]["items"]:
        data = item.get("data", {})
        deps = data.get("previousProductsDependency", [])
        previous_dependency = ", ".join(d.get("previousProductName","") for d in deps)

        produtos.append({
            "id": data.get("id"),
            "name": data.get("name"),
            "unit": data.get("unit"),
            "previous_dependency": previous_dependency
        })
    return produtos # retorna os dados estruturados
