# services/ordem_producao_service.py
from repositories.ordem_producao_repository import (
    fetch_all_ordens,
    insert_ordem,
    update_ordem,
    mark_inactive_missing
)
from core.utils import normalize_str
from datetime import datetime

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

def parse_date(dt_str):
    if not dt_str:
        return None
    dt_str = dt_str.strip()
    if dt_str.endswith("Z"):
        dt_str = dt_str[:-1]
    if "." in dt_str:
        dt_str = dt_str.split(".")[0]

    formatos = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y",
    ]

    for fmt in formatos:
        try:
            return datetime.strptime(dt_str, fmt)
        except:
            pass
    return None

def datas_diferentes(d1, d2):
    if d1 is None and d2 is None:
        return False
    if d1 is None or d2 is None:
        return True
    # comparar apenas ano, mês, dia, hora, minuto, segundo
    # transforma date em datetime para comparar
    if isinstance(d1, datetime) is False:
        d1 = datetime(d1.year, d1.month, d1.day)
    if isinstance(d2, datetime) is False:
        d2 = datetime(d2.year, d2.month, d2.day)
    return int(d1.timestamp()) != int(d2.timestamp())

def sync_ordens(conn, itens_api: list, map_prod_api_to_id: dict):
    existente_map = fetch_all_ordens(conn)
    total = len(itens_api)
    inserted = 0
    updated = 0
    alive_ids = []

    for item in itens_api:
        id_aloee = item.get("id_aloee")
        if not id_aloee:
            continue
        alive_ids.append(id_aloee)

        id_produto_aloee = item.get("id_produto_aloee")
        id_produto = map_prod_api_to_id.get(str(id_produto_aloee))
        if id_produto is None:
            continue

        ordem_data = {
            "id_aloee": id_aloee,
            "id_produto": id_produto,
            "id_produto_aloee": id_produto_aloee,
            "situacao": item.get("situacao"),
            "ignorar_planejamento": item.get("ignorar_planejamento"),
            "descricao": item.get("descricao"),
            "cliente": item.get("cliente"),
            "pedido": item.get("pedido"),
            "ficticia": item.get("ficticia"),
            "prioridade": item.get("prioridade"),
            "quantidade": item.get("quantidade"),
            "saldo": item.get("saldo"),
            "data_entrega": parse_date(item.get("data_entrega")),
            "data_inicio": parse_date(item.get("data_inicio")),
            "data_fim": parse_date(item.get("data_fim")),
            "data_pedido": parse_date(item.get("data_pedido")),
            "observacoes": item.get("observacoes")
        }

        # NOVA ORDEM
        if id_aloee not in existente_map:
            try:
                insert_ordem(conn, ordem_data)
                inserted += 1
            except:
                pass
            continue

        # EXISTENTE → VERIFICAR DIFERENÇAS
        row = existente_map[id_aloee]
        changed = False

        # comparar campos de texto
        for campo in ["descricao", "cliente", "pedido", "situacao",
                      "ignorar_planejamento", "ficticia", "observacoes"]:
            val_banco = normalize_str(row.get(campo))
            val_item = normalize_str(ordem_data.get(campo))
            # só considera diferença se banco não estiver vazio
            if val_banco not in ("", None) and val_banco != val_item:
                changed = True
                print(f"[DEBUG] Ordem {id_aloee} difere no campo '{campo}': banco='{val_banco}' | api='{val_item}'")
                break

        # comparar campos numéricos
        if not changed:
            for campo in ["quantidade", "saldo", "prioridade"]:
                val_banco = _safe_float(row.get(campo))
                val_item = _safe_float(ordem_data.get(campo))
                if val_banco is not None and _float_diff(val_banco, val_item):
                    changed = True
                    print(f"[DEBUG] Ordem {id_aloee} difere no campo '{campo}': banco='{val_banco}' | api='{val_item}'")
                    break

        # comparar datas
        if not changed:
            for campo in ["data_entrega", "data_inicio", "data_fim", "data_pedido"]:
                val_banco = row.get(campo)
                val_item = ordem_data.get(campo)
                if val_banco is not None and datas_diferentes(val_banco, val_item):
                    changed = True
                    print(f"[DEBUG] Ordem {id_aloee} difere no campo '{campo}': banco='{val_banco}' | api='{val_item}'")
                    break

        # somente atualiza se realmente mudou algum campo relevante
        if changed:
            try:
                print(f"[DEBUG] Ordem {id_aloee} será atualizada")
                update_ordem(conn, ordem_data)
                updated += 1
            except:
                pass

    try:
        inativados = mark_inactive_missing(conn, alive_ids)
    except:
        inativados = 0

    return {
        "total": total,
        "inseridos": inserted,
        "atualizados": updated,
        "inativados": inativados
    }
