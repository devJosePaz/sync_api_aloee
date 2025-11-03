import traceback
from endpoints.produtos import fetch_produtos
from endpoints.modelos_producao import fetch_modelos_producao
from db.connection import get_connection
from db.upserts import upsert_product, upsert_model
from utils.logger import log_info, write_summary, print_header
from datetime import datetime
import time

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

def countdown_close(seconds=5):
    """Contagem regressiva antes de fechar o console"""
    print("\n")
    for i in range(seconds, 0, -1):
        print(f"Fechando o console em {i}...", end="\r", flush=True)
        time.sleep(1)
    print("Fechando o console... ✔          ")

def main():
    print_header()  
    try:
        conn = get_connection()
        log_info("Conexão com banco estabelecida", status="info")

        # Processa produtos
        produtos_total, produtos_inseridos, produtos_atualizados, map_prod_api_to_id = process_produtos(conn)

        # Processa modelos
        modelos_total, modelos_inseridos, modelos_atualizados = process_modelos(conn, map_prod_api_to_id)

        conn.commit()
        log_info("Commit finalizado com sucesso", status="info")
        log_info("Sincronização concluída", status="info")

        # Resumo final do dia
        write_summary(
            produtos_total=produtos_total,
            produtos_inseridos=produtos_inseridos,
            produtos_atualizados=produtos_atualizados,
            modelos_total=modelos_total,
            modelos_inseridos=modelos_inseridos,
            modelos_atualizados=modelos_atualizados
        )

        # Contagem regressiva antes de fechar
        countdown_close(3)

    except Exception as e:
        log_info(f"ERRO GERAL: {e}", status="error")
        log_info(traceback.format_exc(), status="error")
        try:
            conn.rollback()
            log_info("Rollback executado com sucesso", status="warning")
        except:
            log_info("Falha ao executar rollback", status="error")
    finally:
        try:
            conn.close()
            log_info("Conexão encerrada", status="info")
        except:
            pass

if __name__ == "__main__":
    main()
