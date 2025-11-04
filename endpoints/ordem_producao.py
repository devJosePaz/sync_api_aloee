from utils.api_client import get_data

def fetch_ordem_producao(page_number=1, page_size=500):
    resp = get_data("/v1/ProductionOrder", page_number, page_size)
    if not resp or "collection" not in resp or "items" not in resp["collection"]:
        return []
    
    ordem_procucao = []
    for item in ["colecttion"]["items"]:
        data = item.get("data", {})
        ordem_procucao.append({
            "id": data.get("id"),
            "name": data.get("name"),
            "product_api_id": data.get("productId"),
            "expectedProductionQuantity": data.get("expectedProductionQuantity"),
            "productionQuantityBalance": data.get( "productionQuantityBalance"),
            "deliveryDate": data.get("deliveryDate")
        })
      

   
