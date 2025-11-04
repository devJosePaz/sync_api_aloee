from utils.logger import log_info
from endpoints.modelos_producao import fetch_modelos_producao
from db.upserts import upsert_model


def process_modelos(conn, map_prod_api_to_id):
    log_info("Iniciando busca de modelos de produção", status="info")
    modelos = fetch_modelos_producao()
    cursor = conn.cursor()

    # Marca todos modelos como inativos antes da atualização
    cursor.execute("UPDATE ModeloOrdem SET Ativo='N'")
    conn.commit()

    inserted = updated = 0
    for m in modelos:
        m["product_id"] = map_prod_api_to_id.get(m.get("product_api_id"))
        m["product_api_id"] = m.get("product_api_id")

        if m["product_id"] is None:
            log_info(f"Produto da API não encontrado: {m.get('product_api_id')}", status="warning")
            continue

        id_modord = upsert_model(conn, m)
        updated += 1
        inserted += 1 if id_modord else 0

    # Atualiza ativos
    ids_api = [m["id"] for m in modelos if m.get("product_id")]
    if ids_api:
        placeholders = ",".join(["?"] * len(ids_api))
        cursor.execute(f"UPDATE ModeloOrdem SET Ativo='S' WHERE IdModeloAloee IN ({placeholders})", ids_api)
        conn.commit()

    log_info(f"[Modelos] Processamento concluído", status="info")
    return len(modelos), inserted, updated