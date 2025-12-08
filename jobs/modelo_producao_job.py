from api.endpoints.modelo_producao import fetch_modelos_producao_api
from services.modelo_producao_service import sync_modelos_producao
from core.logger import log_info

def run_modelo_producao_job(conn, map_prod_api_to_id):
    log_info("JOB modelo de produção: iniciando sincronização", "info")
    itens = fetch_modelos_producao_api()
    log_info(f"JOB modelo de produção: {len(itens)} itens obtidos da API", "info")
    result = sync_modelos_producao(conn, itens, map_prod_api_to_id)
    log_info("JOB modelo de produção: finalizado", "info")
    return result
