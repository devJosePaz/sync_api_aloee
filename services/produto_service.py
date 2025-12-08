# services/produto_service.py
from repositories.produto_repository import (
    fetch_all_produtos,
    insert_produto,
    update_produto,
    mark_inactive_missing
)
from core.logger import log_info

def sync_produtos(conn, itens_api: list):
    """
    Faz o sync dos produtos.
    Retorna dict com métricas e mapa IdProdutoAloee -> IdProduto interno.
    """
    log_info("Service: carregando produtos existentes do banco", "info")
    existente_map = fetch_all_produtos(conn)  # {id_aloee: {...}}

    total = len(itens_api)
    inserted = 0
    updated = 0

    # map produto aloee -> id interno
    map_prod_api_to_id = {k: v["IdProduto"] for k, v in existente_map.items()}

    alive_ids = []

    for item in itens_api:
        id_aloee = item.get("id_aloee")
        if not id_aloee:
            log_info(f"Produto sem id_aloee ignorado: {item}", "warning")
            continue

        alive_ids.append(id_aloee)

        if id_aloee not in existente_map:
            # inserir
            try:
                new_id = insert_produto(conn, item)
                map_prod_api_to_id[id_aloee] = new_id
                inserted += 1
                log_info(f"Produto inserido: {item.get('descricao')} (IdProduto={new_id})", "info")
            except Exception as e:
                log_info(f"Erro ao inserir produto {id_aloee}: {e}", "error")
        else:
            # comparar e atualizar somente se necessário (pode-se comparar campo a campo)
            row = existente_map[id_aloee]
            changed = False
            # lista simples de campos para comparar
            campos = ["Descricao", "Unidade", "Dependencia", "IdProdutoDepAloee"]
            # map de item para formato do banco
            banco_vals = {
                "Descricao": row.get("Descricao"),
                "Unidade": row.get("Unidade"),
                "Dependencia": row.get("Dependencia"),
                "IdProdutoDepAloee": row.get("IdProdutoDepAloee") if row.get("IdProdutoDepAloee") else None
            }
            item_vals = {
                "Descricao": item.get("descricao"),
                "Unidade": item.get("unidade"),
                "Dependencia": item.get("dependencia_nome"),
                "IdProdutoDepAloee": item.get("dependencia_id_aloee")
            }
            for f in campos:
                # tratar None/""
                if (banco_vals.get(f) or "") != (item_vals.get(f) or ""):
                    changed = True
                    break

            if changed:
                try:
                    update_produto(conn, {
                        "id_aloee": id_aloee,
                        "descricao": item.get("descricao"),
                        "unidade": item.get("unidade"),
                        "dependencia_nome": item.get("dependencia_nome"),
                        "dependencia_id_aloee": item.get("dependencia_id_aloee")
                    })
                    updated += 1
                    log_info(f"Produto atualizado: {item.get('descricao')} (IdProdutoAloee={id_aloee})", "info")
                except Exception as e:
                    log_info(f"Erro ao atualizar produto {id_aloee}: {e}", "error")

    # marcar inativos
    try:
        inativados = mark_inactive_missing(conn, alive_ids)
        log_info(f"Produtos marcados como inativos: {inativados}", "info")
    except Exception as e:
        log_info(f"Erro ao marcar produtos inativos: {e}", "error")
        inativados = 0

    metrics = {
        "total": total,
        "inseridos": inserted,
        "atualizados": updated,
        "inativados": inativados,
        "map_prod_api_to_id": map_prod_api_to_id
    }
    return metrics
