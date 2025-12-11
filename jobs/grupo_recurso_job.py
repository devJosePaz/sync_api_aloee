#jobs/grupo_recurso_job.py
from api.endpoints.grupo_recurso import fetch_grupos_recurso_api
from services.grupo_recurso_service import sync_grupos_recurso
from core.logger import log_info


def run_grupo_recurso_job(conn):
    log_info("JOB grupo_recurso: iniciando sincronização", "info")
    itens = fetch_grupos_recurso_api()
    log_info(f"JOB grupo_recurso: {len(itens)} itens obtidos da API", "info")
    result = sync_grupos_recurso(conn, itens)
    log_info("JOB grupo_recurso: finalizado", "info")
    
    return result
