#services/ordem_operacao_service.py
from repositories.ordem_operacao_repository import (
    fetch_all_ordens,
    insert_ordem,
    update_ordem,
    mark_inactive_missing
)
from repositories.grupo_recurso_repository import fetch_all_grupos
from core.logger import log_info
from core.utils import normalize_str, normalize_uuid

def sync_ordens_operacao(conn, itens_api, map_prod_api_to_id):
    """
    Faz o sync das ordens de operação de forma cirúrgica.
    Retorna dict com métricas e mapa IdOrdemProducaoOpeAloee -> IdOrdemProducaoOpe interno.
    """
    log_info("Service: carregando ordens existentes do banco", "info")
    existente_map = fetch_all_ordens(conn)  # {id_aloee: {...}}

    # Mapas para resolver IDs internos
    ordens_producao_map = {k: v["IdOrdemProducao"] for k, v in fetch_all_ordens(conn).items()}
    grupos_recurso_map = {k: v["IdGrupoRecurso"] for k, v in fetch_all_grupos(conn).items()}

    total = len(itens_api)
    inserted = 0
    updated = 0
    alive_ids = []

    campos = [
        "Situacao", "Descricao", "Nivel", "QuantidadeVariavel", "Quantidade",
        "Unidade", "TempoVariavel", "TempoProducao", "TempoSetupFixo",
        "TempoSetupVariavel", "TempoMaxParada", "TempoMinProxima", "TempoMaxProxima",
        "LoteTransferencia", "Observacoes", "DataColeta", "QtdBoa",
        "QtdRetrabalho", "QtdSucata", "QtdUnitaria", "TempoProdDecorrido",
        "TempoProdReal", "TempoParadaPlanejadoReal", "TempoParadaNaoPlanejadoReal",
        "TempoSetupReal"
    ]

    map_api_to_id = {k: v["IdOrdemProducaoOpe"] for k, v in existente_map.items()}

    for item in itens_api:
        id_aloee = item.get("id_ordem_producao_ope_aloee")
        if not id_aloee:
            log_info(f"Ordem sem id_ordem_producao_ope_aloee ignorada: {item}", "warning")
            continue

        alive_ids.append(id_aloee)

        # Resolver IDs internos
        id_ordem_interno = map_prod_api_to_id.get(item.get("id_ordem_producao_aloee"))
        id_grupo_interno = grupos_recurso_map.get(item.get("id_grupo_recurso_aloee"))

        if not id_ordem_interno or not id_grupo_interno:
            log_info(f"IDs internos não encontrados para ordem {id_aloee}", "warning")
            continue

        if id_aloee not in existente_map:
            # Inserir nova ordem
            try:
                new_id = insert_ordem(conn, item, id_ordem_interno, id_grupo_interno)
                map_api_to_id[id_aloee] = new_id
                inserted += 1
                log_info(f"Ordem inserida: {item.get('descricao')} (Id={new_id})", "info")
            except Exception as e:
                log_info(f"Erro ao inserir ordem {id_aloee}: {e}", "error")
        else:
            # Verificar se precisa atualizar
            row = existente_map[id_aloee]
            changed = False

            banco_vals = {f: row.get(f) for f in campos}
            item_vals = {f: item.get(f.lower()) for f in campos}  # campos da API em snake_case

            for f in campos:
                val_banco = normalize_str(banco_vals[f]) if banco_vals[f] is not None else None
                val_item = normalize_str(item_vals[f]) if item_vals[f] is not None else None
                if val_banco != val_item:
                    log_info(f"Diff detectado no campo '{f}': banco='{val_banco}' | api='{val_item}'", "info")
                    changed = True
                    break

            if changed:
                try:
                    update_ordem(conn, item, id_ordem_interno, id_grupo_interno)
                    updated += 1
                    log_info(f"Ordem atualizada: {item.get('descricao')} (IdOrdemAloee={id_aloee})", "info")
                except Exception as e:
                    log_info(f"Erro ao atualizar ordem {id_aloee}: {e}", "error")

    # Marcar ordens inativas
    try:
        inativados = mark_inactive_missing(conn, alive_ids)
        log_info(f"Ordens marcadas como inativas: {inativados}", "info")
    except Exception as e:
        log_info(f"Erro ao marcar ordens inativas: {e}", "error")
        inativados = 0

    metrics = {
        "total": total,
        "inseridos": inserted,
        "atualizados": updated,
        "inativados": inativados,
        "map_api_to_id": map_api_to_id
    }
    return metrics
