# jobs/ordem_operacao_job.py
from core.db import get_connection
from core.logger import log_info
from services.ordem_operacao_service import sync_ordens_operacao
from repositories.ordem_producao_repository import fetch_all_ordens as fetch_ordens_producao
from repositories.grupo_recurso_repository import fetch_all_grupos

def run_ordem_operacao_job(itens_api, map_ordem_api_to_id, map_grupo_api_to_id):
    """
    Job de sincronização de ordens de operação.
    Apenas orquestra a execução do service.
    """
    log_info("JOB ordem de operação: iniciando sincronização", "info")

    with get_connection() as conn:
        # Sincroniza ordens de operação
        metrics = sync_ordens_operacao(conn, itens_api, map_ordem_api_to_id, map_grupo_api_to_id)

    log_info(
        f"JOB ordem de operação: finalizado | Total={metrics['total']}, "
        f"Inseridos={metrics['inseridos']}, Atualizados={metrics['atualizados']}, "
        f"Inativados={metrics['inativados']}",
        "info"
    )
    return metrics
