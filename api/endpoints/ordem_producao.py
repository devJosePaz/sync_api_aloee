# api/endpoints/ordem_producao.py
from api.client import client

def fetch_ordens_api():
    ordens_agrupadas = []
    for page_items in client.paginate("/v1/ProductionOrder"):
        for entry in page_items:
            d = entry.get("data", {}) if isinstance(entry, dict) else {}
            if not d.get("id") or not d.get("productId"):
                continue  # filtra dados incompletos
            ordens_agrupadas.append({
                "id_aloee": d.get("id"),
                "id_produto_aloee": d.get("productId"),
                "descricao": d.get("name"),
                "situacao": d.get("progressStatus"),
                "ignorar_planejamento": 'S' if d.get("ignoredInScenarios") else 'N',
                "cliente": d.get("customer"),
                "pedido": d.get("salesOrder"),
                "ficticia": 'S' if d.get("isFictitious") else 'N',
                "prioridade": d.get("priority"),
                "quantidade": d.get("expectedProductionQuantity"),
                "saldo": d.get("productionQuantityBalance"),
                "data_entrega": d.get("deliveryDate"),
                "data_inicio": d.get("earlyStart"),
                "data_fim": d.get("laterEnd"),
                "data_pedido": d.get("salesOrderDate"),
                "observacoes": None  # API não fornece por enquanto
            })
    return ordens_agrupadas
