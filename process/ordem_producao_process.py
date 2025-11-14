from utils.logger import log_info
from endpoints.ordem_producao import fetch_ordem_producao
from db.upserts import upsert_model

def process_ordem_producao(conn, map_prod_api_to_id):
    log_info("Buscando Ordem de Produção", status="info")
    ordem = fetch_ordem_producao()
    cursor = conn.cursor()

    pass
  

