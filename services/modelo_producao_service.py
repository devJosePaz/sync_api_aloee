# services/modelo_producao_service.py
from repositories.modelo_producao_repository import (
    fetch_all_modelos_producao,
    insert_modelo_producao,
    update_modelo_producao,
    mark_inactive_missing_modelo_producao
)
from core.logger import log_info
from core.utils import normalize_str, normalize_uuid

def sync_modelos_producao(conn, itens_api: list, map_prod_api_to_id: dict):
    """
    Faz o sync dos modelos de produção de forma cirúrgica.
    Retorna dict com métricas.
    """
    log_info("Service: carregando modelos de produção existentes do banco", "info")
    existente_map = fetch_all_modelos_producao(conn)  # {id_aloee: {...}}

    total = len(itens_api)
    inserted = 0
    updated = 0
    alive_ids = []

    campos = ["Descricao", "IdProduto"]  # campos que importam para atualização

    for item in itens_api:
        id_aloee = item.get("id_aloee")
        if not id_aloee:
            log_info(f"Modelo sem id_aloee ignorado: {item}", "warning")
            continue

        alive_ids.append(id_aloee)

        # Resolver o IdProduto interno
        id_produto = map_prod_api_to_id.get(item.get("id_produto_aloee"))
        if not id_produto:
            log_info(f"Modelo {id_aloee} ignorado: IdProduto não encontrado para {item.get('id_produto_aloee')}", "warning")
            continue
        item["IdProduto"] = id_produto

        if id_aloee not in existente_map:
            try:
                insert_modelo_producao(conn, item)
                inserted += 1
                log_info(f"Modelo inserido: {item.get('descricao')} (IdProduto={id_produto})", "info")
            except Exception as e:
                log_info(f"Erro ao inserir modelo {id_aloee}: {e}", "error")
        else:
            row = existente_map[id_aloee]
            changed = False

            banco_vals = {
                "Descricao": row.get("Descricao"),
                "IdProduto": row.get("IdProduto")
            }
            item_vals = {
                "Descricao": item.get("descricao"),
                "IdProduto": item.get("IdProduto")
            }

            for f in campos:
                if f == "IdProduto":
                    val_banco = normalize_uuid(banco_vals[f])
                    val_item = normalize_uuid(item_vals[f])
                    if val_banco and val_banco != val_item:
                        log_info(f"Diff detectado no campo '{f}': banco='{val_banco}' | api='{val_item}'", "info")
                        changed = True
                        break
                else:
                    val_banco = normalize_str(banco_vals[f])
                    val_item = normalize_str(item_vals[f])
                    if val_banco != val_item:
                        log_info(f"Diff detectado no campo '{f}': banco='{val_banco}' | api='{val_item}'", "info")
                        changed = True
                        break

            if changed:
                try:
                    update_modelo_producao(conn, {
                        "id_aloee": id_aloee,
                        "descricao": item.get("descricao"),
                        "id_produto": item.get("IdProduto")
                    })
                    updated += 1
                    log_info(f"Modelo atualizado: {item.get('descricao')} (IdProdutoAloee={id_aloee})", "info")
                except Exception as e:
                    log_info(f"Erro ao atualizar modelo {id_aloee}: {e}", "error")

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
