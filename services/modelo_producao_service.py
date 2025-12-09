from repositories.modelo_producao_repository import (
    fetch_all_modelos_producao,
    insert_modelo_producao,
    update_modelo_producao,
    mark_inactive_missing_modelo_producao
)

from core.logger import log_info

def sync_modelos_producao(conn, itens_api: list, map_prod_api_to_id: dict):
    """
    Faz o sync dos modelos de produção.
    Recebe o mapa de IdProdutoAloee -> IdProduto interno para relacionamentos.
    """
    log_info("Service: carregando modelos de produção existentes do banco", "info")
    existente_map = fetch_all_modelos_producao(conn)  # {id_modelo_aloee: {...}}

    total = len(itens_api)
    inserted = 0
    updated = 0
    alive_ids = []

    for item in itens_api:
        id_modelo_aloee = item.get("id_aloee")
        id_produto_aloee = item.get("id_produto_aloee")
        id_produto_interno = map_prod_api_to_id.get(id_produto_aloee)

        if not id_produto_interno:
            log_info(f"Modelo {id_modelo_aloee} ignorado: IdProduto não encontrado para {id_produto_aloee}", "warning")
            continue

        alive_ids.append(id_modelo_aloee)

        modelo_data = {
            "id_aloee": id_modelo_aloee,
            "id_produto_aloee": id_produto_aloee,
            "id_produto": id_produto_interno,
            "descricao": item.get("descricao"),
            "cliente": item.get("cliente"),
            "quantidade": item.get("quantidade"),
            "observacoes": item.get("observacoes"),
            "ativo": item.get("ativo", "S")
        }

        if id_modelo_aloee not in existente_map:
            # Inserir novo modelo
            try:
                insert_modelo_producao(conn, modelo_data)
                inserted += 1
                log_info(f"Modelo inserido: {modelo_data['descricao']} (IdModeloOrdemAloee={id_modelo_aloee})", "info")
            except Exception as e:
                log_info(f"Erro ao inserir modelo {id_modelo_aloee}: {e}", "error")
        else:
            # Atualizar existente
            try:
                update_modelo_producao(conn, modelo_data)
                updated += 1
                log_info(f"Modelo atualizado: {modelo_data['descricao']} (IdModeloOrdemAloee={id_modelo_aloee})", "info")
            except Exception as e:
                log_info(f"Erro ao atualizar modelo {id_modelo_aloee}: {e}", "error")

    # Marcar modelos inativos
    try:
        inativados = mark_inactive_missing_modelo_producao(conn, alive_ids)
        log_info(f"Modelos marcados como inativos: {inativados}", "info")
    except Exception as e:
        log_info(f"Erro ao marcar modelos inativos: {e}", "error")
        inativados = 0

    return {
        "total": total,
        "inseridos": inserted,
        "atualizados": updated,
        "inativados": inativados
    }
