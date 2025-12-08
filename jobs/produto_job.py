from api.endpoints.produto import fetch_produtos_api
from services.produto_service import sync_produtos
from core.logger import log_info

def run_produto_job(conn):
    log_info("JOB produto: iniciando sincronização", "info")
    itens = fetch_produtos_api()
    log_info(f"JOB produto: {len(itens)} itens obtidos da API", "info")
    result = sync_produtos(conn, itens)
    log_info("JOB produto: finalizado", "info")
    return result
