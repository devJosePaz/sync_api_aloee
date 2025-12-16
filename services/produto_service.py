from repositories.produto_repository import (
    fetch_all_produtos,
    insert_produto,
    update_produto,
    mark_inactive_missing
)
from core.logger import log_info
from core.utils import normalize_str


def sync_produtos(conn, itens_api: list):
    """
    Faz o sync dos produtos de forma segura.
    Retorna dict com métricas e mapa IdProdutoAloee -> IdProduto interno.
    """
    log_info("Service: carregando produtos existentes do banco", "info")
    existente_map = fetch_all_produtos(conn)  # {id_aloee: {...}}

    total = len(itens_api)
    inserted = 0
    updated = 0
    map_prod_api_to_id = {k: v["IdProduto"] for k, v in existente_map.items()}
    alive_ids = []

    # Somente campos relevantes para decidir UPDATE
    campos_diff = ["Descricao", "Unidade"]

    for item in itens_api:
        id_aloee = item.get("id_aloee")
        if not id_aloee:
            log_info(f"Produto sem id_aloee ignorado: {item}", "warning")
            continue

        alive_ids.append(id_aloee)

        # ----------------------------
        # DEPENDÊNCIA (RESOLUÇÃO RELACIONAL)
        # ----------------------------

        dependencia_id_aloee = item.get("dependencia_id_aloee")

        # FK interna
        dep_interno = (
            map_prod_api_to_id.get(dependencia_id_aloee)
            if dependencia_id_aloee
            else None
        )

        # Resolve o NOME DA DEPENDÊNCIA VIA TABELA (não via API)
        dependencia_descricao = None
        if dep_interno:
            for v in existente_map.values():
                if v["IdProduto"] == dep_interno:
                    dependencia_descricao = v["Descricao"]
                    break

        # Campos que o repository espera
        item["dependencia_id_aloee"] = dependencia_id_aloee
        item["dependencia_descricao"] = dependencia_descricao

        # ----------------------------
        # INSERT
        # ----------------------------
        if id_aloee not in existente_map:
            try:
                new_id = insert_produto(conn, item, map_prod_api_to_id)
                map_prod_api_to_id[id_aloee] = new_id
                inserted += 1
                log_info(
                    f"Produto inserido: {item.get('descricao')} (IdProduto={new_id})",
                    "info"
                )
            except Exception as e:
                log_info(f"Erro ao inserir produto {id_aloee}: {e}", "error")

        # ----------------------------
        # UPDATE
        # ----------------------------
        else:
            row = existente_map[id_aloee]
            changed = False

            banco_vals = {
                "Descricao": row.get("Descricao"),
                "Unidade": row.get("Unidade"),
            }

            item_vals = {
                "Descricao": item.get("descricao"),
                "Unidade": item.get("unidade"),
            }

            for f in campos_diff:
                val_banco = normalize_str(banco_vals[f])
                val_item = normalize_str(item_vals[f])
                if val_banco != val_item:
                    log_info(
                        f"Diff detectado no campo '{f}': "
                        f"banco='{val_banco}' | api='{val_item}'",
                        "info"
                    )
                    changed = True
                    break

            # UPDATE acontece se:
            # - houve diff real
            # OU
            # - existe dependência resolvida (para garantir persistência dos campos legados)
            if changed or dep_interno:
                try:
                    update_produto(conn, item, map_prod_api_to_id)
                    updated += 1
                    log_info(
                        f"Produto atualizado: {item.get('descricao')} "
                        f"(IdProdutoAloee={id_aloee})",
                        "info"
                    )
                except Exception as e:
                    log_info(f"Erro ao atualizar produto {id_aloee}: {e}", "error")

    # ----------------------------
    # INATIVAÇÃO
    # ----------------------------
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
