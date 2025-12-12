# services/modelo_producao_service.py
from repositories.modelo_producao_repository import (
    fetch_all_modelos,
    insert_modelo,
    update_modelo,
    mark_inactive_missing
)
from core.logger import log_info
from core.utils import normalize_str, normalize_uuid

def _safe_float(v):
    try:
        return float(v) if v is not None else None
    except Exception:
        return None

def _float_diff(a, b, eps=1e-9):
    if a is None and b is None:
        return False
    if a is None or b is None:
        return True
    return abs(a - b) > eps

# Função de sincronização com controle de exceções mais robusto
def sync_modelos_producao(conn, itens_api: list, map_prod_api_to_id: dict):
    log_info("Service: carregando modelos existentes do banco", "info")
    existente_map = fetch_all_modelos(conn)  # {id_modelo_aloee: {...}}

    total = len(itens_api)
    inserted = 0
    updated = 0
    alive_ids = []

    map_modelo_api_to_id = {k: v["IdModeloOrdem"] for k, v in existente_map.items()}

    campos = ["Descricao", "Cliente", "Observacoes", "IdProdutoAloee"]

    for item in itens_api:
        id_modelo = item.get("id_modelo_aloee")
        if not id_modelo:
            log_info(f"Modelo sem id_modelo_aloee ignorado: {item}", "warning")
            continue

        alive_ids.append(id_modelo)

        id_produto_aloee = item.get("id_produto_aloee")
        id_produto_interno = map_prod_api_to_id.get(str(id_produto_aloee)) if id_produto_aloee else None
        if id_produto_interno is None:
            log_info(f"FK produto não resolvida para modelo {id_modelo}", "warning")
            continue

        if id_modelo not in existente_map:
            try:
                new_id = insert_modelo(conn, item, id_produto_interno)
                map_modelo_api_to_id[id_modelo] = new_id
                inserted += 1
                log_info(f"Modelo inserido: {item.get('descricao')} (IdModeloOrdem={new_id})", "info")
            except Exception as e:
                log_info(f"Erro ao inserir modelo {id_modelo}: {e}", "error")
        else:
            row = existente_map[id_modelo]
            changed = False

            banco_vals = {
                "Descricao": row.get("Descricao"),
                "Cliente": row.get("Cliente"),
                "Observacoes": row.get("Observacoes"),
                "IdProdutoAloee": row.get("IdProdutoAloee"),
                "Quantidade": row.get("Quantidade")
            }
            item_vals = {
                "Descricao": item.get("descricao"),
                "Cliente": item.get("cliente"),
                "Observacoes": item.get("observacoes"),
                "IdProdutoAloee": item.get("id_produto_aloee"),
                "Quantidade": _safe_float(item.get("quantidade"))
            }

            for f in campos:
                if f == "IdProdutoAloee":
                    val_banco = normalize_uuid(banco_vals[f])
                    val_item = normalize_uuid(item_vals[f])
                    if val_banco != val_item:
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

            if not changed:
                val_banco_q = _safe_float(banco_vals["Quantidade"])
                val_item_q = item_vals["Quantidade"]
                if _float_diff(val_banco_q, val_item_q):
                    log_info(f"Diff detectado no campo 'Quantidade': banco='{val_banco_q}' | api='{val_item_q}'", "info")
                    changed = True

            if changed:
                try:
                    update_modelo(conn, {
                        "id_modelo_aloee": id_modelo,
                        "id_produto_aloee": item.get("id_produto_aloee"),
                        "descricao": item.get("descricao"),
                        "cliente": item.get("cliente"),
                        "quantidade": item.get("quantidade"),
                        "observacoes": item.get("observacoes")
                    }, id_produto_interno)
                    updated += 1
                    log_info(f"Modelo atualizado: {item.get('descricao')} (IdModeloOrdemAloee={id_modelo})", "info")
                except Exception as e:
                    log_info(f"Erro ao atualizar modelo {id_modelo}: {e}", "error")

    try:
        inativados = mark_inactive_missing(conn, alive_ids)
        log_info(f"Modelos marcados como inativos: {inativados}", "info")
    except Exception as e:
        log_info(f"Erro ao marcar modelos inativos: {e}", "error")
        inativados = 0

    metrics = {
        "total": total,
        "inseridos": inserted,
        "atualizados": updated,
        "inativados": inativados,
        "map_modelo_api_to_id": map_modelo_api_to_id
    }
    return metrics
