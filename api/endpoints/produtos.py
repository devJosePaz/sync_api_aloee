from api.client import client

def fetch_products():
    resp = client.get("/v1/Product")
    if not resp or "collection" not in resp:
        return []

    items = resp["collection"]["items"]
    result = []

    for i in items:
        d = i.get("data", {})
        deps = d.get("previousProductsDependency", [])

        result.append({
            "id": d.get("id"),
            "name": d.get("name"),
            "unit": d.get("unit"),
            "previous_dependency": ", ".join(x["previousProductName"] for x in deps)
        })
    
    return result
