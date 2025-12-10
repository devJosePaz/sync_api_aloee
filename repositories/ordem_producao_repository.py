# repositories/ordem_producao_repository.py
from core.db import get_connection

TABLE = "Al_OrdemProducao"


def fetch_all_ordens(conn):
    cur = conn.cursor()
    cur.execute(f"""
        SELECT
            IdOrdemProducao,
            IdOrdemProducaoAloee,
            IdProduto,
            IdProdutoAloee,
            Situacao,
            IgnorarPlanejamento,
            Descricao,
            Cliente,
            Pedido,
            Ficticia,
            Prioridade,
            Quantidade,
            Saldo,
            DataEntrega,
            DataInicio,
            DataFim,
            DataPedido,
            Observacoes,
            Ativo
        FROM {TABLE}
    """)
    rows = cur.fetchall()

    result = {}
    for r in rows:
        result[str(r[1])] = {
            "IdOrdemProducao": r[0],
            "IdOrdemProducaoAloee": r[1],
            "IdProduto": r[2],
            "IdProdutoAloee": r[3],
            "Situacao": r[4],
            "IgnorarPlanejamento": r[5],
            "Descricao": r[6],
            "Cliente": r[7],
            "Pedido": r[8],
            "Ficticia": r[9],
            "Prioridade": r[10],
            "Quantidade": r[11],
            "Saldo": r[12],
            "DataEntrega": r[13],
            "DataInicio": r[14],
            "DataFim": r[15],
            "DataPedido": r[16],
            "Observacoes": r[17],
            "Ativo": r[18]
        }
    return result


def insert_ordem(conn, item):
    cur = conn.cursor()
    cur.execute(f"""
        INSERT INTO {TABLE} (
            IdOrdemProducaoAloee,
            IdProduto,
            IdProdutoAloee,
            Situacao,
            IgnorarPlanejamento,
            Descricao,
            Cliente,
            Pedido,
            Ficticia,
            Prioridade,
            Quantidade,
            Saldo,
            DataEntrega,
            DataInicio,
            DataFim,
            DataPedido,
            Observacoes,
            Ativo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item.get("id_aloee"),
        item.get("id_produto"),
        item.get("id_produto_aloee"),
        item.get("situacao"),
        item.get("ignorar_planejamento"),
        item.get("descricao"),
        item.get("cliente"),
        item.get("pedido"),
        item.get("ficticia"),
        item.get("prioridade"),
        item.get("quantidade"),
        item.get("saldo"),
        item.get("data_entrega"),
        item.get("data_inicio"),
        item.get("data_fim"),
        item.get("data_pedido"),
        item.get("observacoes"),
        'S'
    ))
    
    # Pega o ID gerado corretamente
    cur.execute(f"SELECT TOP 1 IdOrdemProducao FROM {TABLE} ORDER BY IdOrdemProducao DESC")
    return cur.fetchone()[0]



def update_ordem(conn, item):
    cur = conn.cursor()
    cur.execute(f"""
        UPDATE {TABLE}
        SET
            IdProduto = ?,
            IdProdutoAloee = ?,
            Situacao = ?,
            IgnorarPlanejamento = ?,
            Descricao = ?,
            Cliente = ?,
            Pedido = ?,
            Ficticia = ?,
            Prioridade = ?,
            Quantidade = ?,
            Saldo = ?,
            DataEntrega = ?,
            DataInicio = ?,
            DataFim = ?,
            DataPedido = ?,
            Observacoes = ?,
            Ativo = ?
        WHERE IdOrdemProducaoAloee = ?
    """, (
        item.get("id_produto"),
        item.get("id_produto_aloee"),
        item.get("situacao"),
        item.get("ignorar_planejamento"),
        item.get("descricao"),
        item.get("cliente"),
        item.get("pedido"),
        item.get("ficticia"),
        item.get("prioridade"),
        item.get("quantidade"),
        item.get("saldo"),
        item.get("data_entrega"),
        item.get("data_inicio"),
        item.get("data_fim"),
        item.get("data_pedido"),
        item.get("observacoes"),
        'S',
        item.get("id_aloee")
    ))
    return cur.rowcount


def mark_inactive_missing(conn, alive_aloee_ids):
    if not alive_aloee_ids:
        return 0

    placeholders = ",".join("?" for _ in alive_aloee_ids)
    cur = conn.cursor()
    cur.execute(
        f"UPDATE {TABLE} SET Ativo='N' WHERE IdOrdemProducaoAloee NOT IN ({placeholders})",
        alive_aloee_ids
    )
    return cur.rowcount
