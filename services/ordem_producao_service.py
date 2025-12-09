# services/ordem_producao_service.py
from repositories.ordem_producao_repository import (
    fetch_all_ordens,
    insert_ordem,
    update_ordem,
    mark_inactive_missing
)
from core.logger import log_info
from core.utils import normalize_str
from datetime import datetime

def parse_date(dt_str):
    """
    Converte string para datetime compatível com SQL Server.
    Retorna None se a string for inválida ou vazia.
    """
    if not dt_str:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(dt_str, fmt)
        except Exception:
            continue
    log_info(f"Data inválida ignorada: {dt_str}", "warning")
    return None

def sync_ordens(conn, itens_api: list, map_prod_api_to_id: dict):
    """
    Faz o sync das ordens de produção.
    map_prod_api_to_id -> {IdProdutoAloee: IdProduto interno}
    """
    log_info("Service: carregando ordens existentes do banco", "info")
    existente_map = fetch_all_ordens(conn)  # {IdOrdemProducaoAloee: {...}}

    total = len(itens_api)
    inserted = 0
    updated = 0
    alive_ids = []

    for item in itens_api:
        id_aloee = item.get("id_aloee")
        if not id_aloee:
            log_info(f"Ordem sem id_aloee ignorada: {item}", "warning")
            continue

        alive_ids.append(id_aloee)

        # Converter datas
        data_entrega = parse_date(item.get("data_entrega"))
        data_inicio = parse_date(item.get("data_inicio"))
        data_fim = parse_date(item.get("data_fim"))

        # Mapear IdProduto interno
        id_produto = map_prod_api_to_id.get(item.get("id_produto_aloee"))

        ordem_data = {
            "id_aloee": id_aloee,
            "id_produto": id_produto,
            "situacao": item.get("situacao"),
            "ignorar_planejamento": item.get("ignorar_planejamento"),
            "descricao": item.get("descricao"),
            "cliente": item.get("cliente"),
            "pedido": item.get("pedido"),
            "ficticia": item.get("ficticia"),
            "prioridade": item.get("prioridade"),
            "quantidade": item.get("quantidade"),
            "saldo": item.get("saldo"),
            "data_entrega": data_entrega,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "data_pedido": parse_date(item.get("data_pedido")),
            "observacoes": item.get("observacoes")
        }

        if id_aloee not in existente_map:
            # Inserir nova ordem
            try:
                new_id = insert_ordem(conn, ordem_data)
                inserted += 1
                log_info(f"Ordem inserida: {ordem_data.get('descricao')} (IdOrdem={new_id})", "info")
            except Exception as e:
                log_info(f"Erro ao inserir ordem {id_aloee}: {e}", "error")
        else:
            # Atualizar ordem existente se necessário
            row = existente_map[id_aloee]
            changed = False

            for campo in ["descricao", "cliente", "pedido", "situacao", "quantidade", "saldo"]:
                val_banco = normalize_str(row.get(campo))
                val_item = normalize_str(ordem_data.get(campo))
                if val_banco != val_item:
                    changed = True
                    log_info(f"Diff detectado no campo '{campo}': banco='{val_banco}' | api='{val_item}'", "info")
                    break

            if changed:
                try:
                    update_ordem(conn, ordem_data)
                    updated += 1
                    log_info(f"Ordem atualizada: {ordem_data.get('descricao')} (IdOrdemAloee={id_aloee})", "info")
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
        "inativados": inativados
    }
    return metrics
