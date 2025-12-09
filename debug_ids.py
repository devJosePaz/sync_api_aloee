# debug_ids.py  -> execute com python debug_ids.py ou cole na sessão
from api.client import client

# amostra de produtos
prod_ids = []
for page in client.paginate("/v1/Product"):
    for e in page:
        d = e.get("data", {}) if isinstance(e, dict) else {}
        prod_ids.append(d.get("id"))
        if len(prod_ids) >= 10:
            break
    if len(prod_ids) >= 10:
        break

print("Amostra ids de /v1/Product:", prod_ids)

# amostra de modelos
modelo_ids = []
modelo_prod_ids = []
for page in client.paginate("/v1/ProductionOrderTemplate"):
    for e in page:
        d = e.get("data", {}) if isinstance(e, dict) else {}
        modelo_ids.append(d.get("id"))
        modelo_prod_ids.append(d.get("productId"))
        if len(modelo_ids) >= 10:
            break
    if len(modelo_ids) >= 10:
        break

print("Amostra ids de /v1/ProductionOrderTemplate (id):", modelo_ids)
print("Amostra productId em modelos:", modelo_prod_ids)
