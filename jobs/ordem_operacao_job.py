# jobs/ordem_operacao_job.py
from api.endpoints.ordem_operacao import fetch_ordens_operacao_api
from services.ordem_operacao_service import sync_ordens_operacao
from core.logger import log_info

def run_ordem_operacao_job(conn, map_ordem_api_to_id):
    log_info("JOB ordem de operação: iniciando sincronização", "info")
    itens = fetch_ordens_operacao_api()
    log_info(f"JOB ordem de operação: {len(itens)} itens obtidos da API", "info")
    result = sync_ordens_operacao(conn, itens, map_ordem_api_to_id)
    log_info("JOB ordem de operação: finalizado", "info")
    return result
