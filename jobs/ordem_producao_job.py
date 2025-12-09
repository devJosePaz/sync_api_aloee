# jobs/ordem_producao_job.py
from api.endpoints.ordem_producao import fetch_ordens_api
from services.ordem_producao_service import sync_ordens
from core.logger import log_info

def run_ordem_producao_job(conn, map_prod_api_to_id):
    log_info("JOB ordem de produção: iniciando sincronização", "info")
    itens = fetch_ordens_api()
    log_info(f"JOB ordem de produção: {len(itens)} itens obtidos da API", "info")
    result = sync_ordens(conn, itens, map_prod_api_to_id)
    log_info("JOB ordem de produção: finalizado", "info")
    return result
