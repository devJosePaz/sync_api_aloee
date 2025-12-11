#services/grupo_recurso_service.py
from repositories.grupo_recurso_repository import (
    fetch_all_grupos,
    insert_grupo,
    update_grupo,
    mark_inactive_missing
)
from core.logger import log_info
from core.utils import normalize_str, normalize_uuid


def sync_grupos_recurso(conn, itens_api: list):
    """
    Sincroniza grupos de recurso com operação cirúrgica.
    Retorna métricas simples.
    """
    log_info("Service: carregando grupos de recurso existentes do banco", "info")
    existente_map = fetch_all_grupos(conn)  # {id_aloee: {...}}

    total = len(itens_api)
    inserted = 0
    updated = 0

    alive_ids = []

    # Campos que serão comparados
    campos = [
        "Descricao",
        "Restricao",
        "Unidade",
        "Quantidade",
        "Maximo",
        "LimitesOee",
        "LimiteA",
        "LimiteB",
        "IdCalendarioAloee"
    ]

    for item in itens_api:
        id_aloee = item.get("id_aloee")
        if not id_aloee:
            log_info(f"GrupoRecurso ignorado por não ter id_aloee: {item}", "warning")
            continue

        alive_ids.append(id_aloee)

        # Novo grupo
        if id_aloee not in existente_map:
            try:
                insert_grupo(conn, item)
                inserted += 1
                log_info(f"GrupoRecurso inserido: {item.get('descricao')}", "info")
            except Exception as e:
                log_info(f"Erro ao inserir GrupoRecurso {id_aloee}: {e}", "error")
            continue

        # Já existe → comparar campos
        row = existente_map[id_aloee]
        changed = False

        banco_vals = {
            "Descricao": row.get("Descricao"),
            "Restricao": row.get("Restricao"),
            "Unidade": row.get("Unidade"),
            "Quantidade": row.get("Quantidade"),
            "Maximo": row.get("Maximo"),
            "LimitesOee": row.get("LimitesOee"),
            "LimiteA": row.get("LimiteA"),
            "LimiteB": row.get("LimiteB"),
            "IdCalendarioAloee": row.get("IdCalendarioAloee"),
        }

        item_vals = {
            "Descricao": item.get("descricao"),
            "Restricao": item.get("restricao"),
            "Unidade": item.get("unidade"),
            "Quantidade": item.get("quantidade"),
            "Maximo": item.get("maximo"),
            "LimitesOee": item.get("limites_oee"),
            "LimiteA": item.get("limite_a"),
            "LimiteB": item.get("limite_b"),
            "IdCalendarioAloee": item.get("id_calendario_aloee")
        }

        for f in campos:
            if f == "IdCalendarioAloee":
                val_banco = normalize_uuid(banco_vals[f])
                val_item = normalize_uuid(item_vals[f])
            else:
                val_banco = normalize_str(banco_vals[f])
                val_item = normalize_str(item_vals[f])

            if val_banco != val_item:
                log_info(
                    f"Diff detectado '{f}': banco='{val_banco}' | api='{val_item}'",
                    "info"
                )
                changed = True
                break

        if changed:
            try:
                update_grupo(conn, {
                    "id_aloee": id_aloee,
                    "descricao": item_vals["Descricao"],
                    "restricao": item_vals["Restricao"],
                    "unidade": item_vals["Unidade"],
                    "quantidade": item_vals["Quantidade"],
                    "maximo": item_vals["Maximo"],
                    "limites_oee": item_vals["LimitesOee"],
                    "limite_a": item_vals["LimiteA"],
                    "limite_b": item_vals["LimiteB"],
                    "id_calendario_aloee": item_vals["IdCalendarioAloee"],
                })
                updated += 1
                log_info(f"GrupoRecurso atualizado: {item_vals['Descricao']}", "info")
            except Exception as e:
                log_info(f"Erro ao atualizar GrupoRecurso {id_aloee}: {e}", "error")

    # Marcar inativos
    try:
        inativados = mark_inactive_missing(conn, alive_ids)
        log_info(f"GruposRecurso inativados: {inativados}", "info")
    except Exception as e:
        log_info(f"Erro ao marcar grupos de recurso inativos: {e}", "error")
        inativados = 0

    return {
        "total": total,
        "inseridos": inserted,
        "atualizados": updated,
        "inativados": inativados
    }
