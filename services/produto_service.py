
from repositories.produto_repository import (
    fetch_all_produtos,
    insert_produto,
    update_produto,
    mark_inactive_missing
)
from core.logger import log_info
from core.utils import normalize_str

def sync_produtos(conn, itens_api: list):
    log_info("Service: carregando produtos existentes do banco", "info")
    existente_map = fetch_all_produtos(conn)  # {id_aloee: {...}}

    total = len(itens_api)
    inserted = 0
    updated = 0

    map_prod_api_to_id = {k: v["IdProduto"] for k, v in existente_map.items()}
    alive_ids = []

    campos_diff = ["Descricao", "Unidade", "Dependencia"]

    for item in itens_api:
        id_aloee = item.get("id_aloee")
        if not id_aloee:
            continue

        alive_ids.append(id_aloee)

        # Resolve dependência
        dep_aloee = item.get("dependencia_id_aloee")
        dep_interno = map_prod_api_to_id.get(dep_aloee) if dep_aloee else None
        item["dependencia_id_interno"] = dep_interno

        # -----------------------
        # INSERT
        # -----------------------
        if id_aloee not in existente_map:
            new_id = insert_produto(conn, item, map_prod_api_to_id)
            map_prod_api_to_id[id_aloee] = new_id
            inserted += 1
            log_info(
                f"Produto inserido: {item.get('descricao')} (IdProduto={new_id})",
                "info"
            )
            continue

        # -----------------------
        # UPDATE (DIFF CORRETO)
        # -----------------------
        row = existente_map[id_aloee]

        banco_vals = {
            "Descricao": row.get("Descricao"),
            "Unidade": row.get("Unidade"),
            "Dependencia": row.get("Dependencia"),
        }

        item_vals = {
            "Descricao": item.get("descricao"),
            "Unidade": item.get("unidade"),
            "Dependencia": dep_interno,
        }

        changed = False

        for campo in campos_diff:
            if campo == "Dependencia":
                val_db = banco_vals[campo]
                val_api = item_vals[campo]
            else:
                val_db = normalize_str(banco_vals[campo])
                val_api = normalize_str(item_vals[campo])

            if val_db != val_api:
                changed = True
                break

        if changed:
            update_produto(conn, item, map_prod_api_to_id)
            updated += 1
            log_info(
                f"Produto atualizado: {item.get('descricao')} (IdProdutoAloee={id_aloee})",
                "info"
            )

    inativados = mark_inactive_missing(conn, alive_ids)

    return {
        "total": total,
        "inseridos": inserted,
        "atualizados": updated,
        "inativados": inativados,
        "map_prod_api_to_id": map_prod_api_to_id
    }
