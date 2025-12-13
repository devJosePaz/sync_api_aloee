from core.db import get_connection
from core.logger import log_info

from api.endpoints.ordem_operacao import fetch_ordem_operacao_api
from repositories.ordem_producao_repository import fetch_all_ordens
from repositories.grupo_recurso_repository import fetch_all_grupos
from services.ordem_operacao_service import sync_ordens_operacao


def run_ordem_operacao_job(conn):  # <-- agora recebe conn
    log_info("Iniciando job de sincronização de Ordens de Operação", "info")

    try:
        itens_api = fetch_ordem_operacao_api()
        if not itens_api:
            log_info("API não retornou Ordens de Operação", "warning")
            return {
                "total": 0,
                "inseridos": 0,
                "atualizados": 0,
                "inativados": 0
            }

        # Mapas COMPLETOS (UUID Aloee -> row do banco)
        map_ordem_producao = fetch_all_ordens(conn)
        map_grupo_recurso = fetch_all_grupos(conn)

        metrics = sync_ordens_operacao(
            conn=conn,
            itens_api=itens_api,
            map_ordem_producao=map_ordem_producao,
            map_grupo_recurso=map_grupo_recurso
        )

        log_info("Job de Ordem de Operação finalizado com sucesso", "info")
        return metrics

    except Exception as e:
        log_info(f"Erro no job de Ordem de Operação: {e}", "error")
        raise
