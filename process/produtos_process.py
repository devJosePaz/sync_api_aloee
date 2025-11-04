from utils.logger import log_info
from endpoints.produtos import fetch_produtos
from db.upserts import upsert_product

def process_produtos(conn):
    log_info("Iniciando busca de produtos", status="info")
    produtos = fetch_produtos()
    cursor = conn.cursor()

    # Marca todos produtos como inativos antes da atualização
    cursor.execute("UPDATE Produto SET Ativo='N'")
    conn.commit()

    inserted = updated = 0
    map_prod_api_to_id = {}

    for p in produtos:
        id_interno = upsert_product(conn, p)
        map_prod_api_to_id[p["id"]] = id_interno
        updated += 1
        inserted += 1 if id_interno not in map_prod_api_to_id.values() else 0

    # Atualiza ativos
    ids_api = list(map_prod_api_to_id.keys())
    if ids_api:
        placeholders = ",".join(["?"] * len(ids_api))
        cursor.execute(f"UPDATE Produto SET Ativo='S' WHERE IdProdAloee IN ({placeholders})", ids_api)
        conn.commit()

    log_info(f"[Produtos] Processamento concluído", status="info")
    return len(produtos), inserted, updated, map_prod_api_to_id

