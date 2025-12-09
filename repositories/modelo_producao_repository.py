# repositories/modelo_ordem_repository.py
from core.db import get_connection

TABLE = "Al_ModeloOrdem"

def fetch_all_modelos(conn):
    """
    Retorna dicionário {IdModeloOrdemAloee: {...}} com colunas:
    IdModeloOrdem, IdModeloOrdemAloee, IdProduto, IdProdutoAloee, Descricao, Cliente, Quantidade, Observacoes, Ativo
    """
    cur = conn.cursor()
    cur.execute(f"""
        SELECT IdModeloOrdem, IdModeloOrdemAloee, IdProduto, IdProdutoAloee,
               Descricao, Cliente, Quantidade, Observacoes, Ativo
        FROM {TABLE}
    """)
    rows = cur.fetchall()
    result = {}
    for r in rows:
        result[str(r[1])] = {
            "IdModeloOrdem": r[0],
            "IdModeloOrdemAloee": r[1],
            "IdProduto": r[2],
            "IdProdutoAloee": r[3],
            "Descricao": r[4],
            "Cliente": r[5],
            "Quantidade": r[6],
            "Observacoes": r[7],
            "Ativo": r[8]
        }
    return result

def get_modelo_by_aloee(conn, id_modelo_aloee):
    cur = conn.cursor()
    cur.execute(f"SELECT IdModeloOrdem FROM {TABLE} WHERE IdModeloOrdemAloee = ?", id_modelo_aloee)
    row = cur.fetchone()
    return row[0] if row else None

def insert_modelo(conn, item, id_produto_interno):
    """
    item: dict vindo da API (campos conforme endpoint)
    id_produto_interno: IdProduto (int) já resolvido pelo map_prod_api_to_id
    """
    cur = conn.cursor()
    cur.execute(f"""
        INSERT INTO {TABLE} (
            IdModeloOrdemAloee,
            IdProduto,
            IdProdutoAloee,
            Descricao,
            Cliente,
            Quantidade,
            Observacoes,
            Ativo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item.get("id_modelo_aloee"),
        id_produto_interno,
        item.get("id_produto_aloee"),
        item.get("descricao"),
        item.get("cliente"),
        item.get("quantidade"),
        item.get("observacoes"),
        'S'
    ))
    cur.execute("SELECT SCOPE_IDENTITY()")
    new_id = cur.fetchone()[0]
    return new_id

def update_modelo(conn, item, id_produto_interno):
    cur = conn.cursor()
    cur.execute(f"""
        UPDATE {TABLE}
        SET
            IdProduto = ?,
            IdProdutoAloee = ?,
            Descricao = ?,
            Cliente = ?,
            Quantidade = ?,
            Observacoes = ?,
            Ativo = ?
        WHERE IdModeloOrdemAloee = ?
    """, (
        id_produto_interno,
        item.get("id_produto_aloee"),
        item.get("descricao"),
        item.get("cliente"),
        item.get("quantidade"),
        item.get("observacoes"),
        'S',
        item.get("id_modelo_aloee")
    ))
    return cur.rowcount

def mark_inactive_missing(conn, alive_aloee_ids: list):
    """
    Marca como Ativo='N' todos modelos cujo IdModeloOrdemAloee nao estiver na lista alive_aloee_ids.
    """
    if not alive_aloee_ids:
        return 0
    placeholders = ",".join("?" for _ in alive_aloee_ids)
    sql = f"UPDATE {TABLE} SET Ativo='N' WHERE IdModeloOrdemAloee NOT IN ({placeholders})"
    cur = conn.cursor()
    cur.execute(sql, alive_aloee_ids)
    return cur.rowcount
