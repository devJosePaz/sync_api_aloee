# repositories/produto_repository.py
from core.db import get_connection

TABLE = "Al_Produto"

def fetch_all_produtos(conn):
    """
    Retorna lista de rows (pyodbc row) ou dicionários com IdProduto, IdProdutoAloee, Descricao, Unidade, Dependencia
    """
    cur = conn.cursor()
    cur.execute(f"SELECT IdProduto, IdProdutoAloee, Descricao, Unidade, Dependencia, Ativo FROM {TABLE}")
    rows = cur.fetchall()
    # transformar para dicionário simples
    result = {}
    for r in rows:
        # pyodbc row -> index access
        # assumindo colunas na ordem selecionada
        result[str(r[1])] = {
            "IdProduto": r[0],
            "IdProdutoAloee": r[1],
            "Descricao": r[2],
            "Unidade": r[3],
            "Dependencia": r[4],
            "Ativo": r[5]
        }
    return result

def get_produto_by_aloee(conn, id_aloee):
    cur = conn.cursor()
    cur.execute(f"SELECT IdProduto FROM {TABLE} WHERE IdProdutoAloee = ?", id_aloee)
    row = cur.fetchone()
    return row[0] if row else None

def insert_produto(conn, item):
    cur = conn.cursor()
    cur.execute(f"""
        INSERT INTO {TABLE} (
            IdProdutoAloee,
            IdProdutoDepAloee,
            CodMaterial,
            Descricao,
            Dependencia,
            Unidade,
            Ativo
        ) VALUES (?, ?, NULL, ?, ?, ?, ?)
    """, (
        item.get("id_aloee"),
        item.get("dependencia_id_aloee"),
        item.get("descricao"),
        item.get("dependencia_nome"),
        item.get("unidade"),
        'S'
    ))
    # pega id gerado
    cur.execute("SELECT SCOPE_IDENTITY()")
    new_id = cur.fetchone()[0]
    return new_id

def update_produto(conn, item):
    cur = conn.cursor()
    cur.execute(f"""
        UPDATE {TABLE}
        SET
            IdProdutoDepAloee = ?,
            Descricao = ?,
            Dependencia = ?,
            Unidade = ?,
            Ativo = ?
        WHERE IdProdutoAloee = ?
    """, (
        item.get("dependencia_id_aloee"),
        item.get("descricao"),
        item.get("dependencia_nome"),
        item.get("unidade"),
        'S',
        item.get("id_aloee")
    ))
    return cur.rowcount

def mark_inactive_missing(conn, alive_aloee_ids: list):
    """
    Marca como Ativo='N' todos produtos cujo IdProdutoAloee nao estiver na lista alive_aloee_ids.
    """
    if not alive_aloee_ids:
        return 0
    placeholders = ",".join("?" for _ in alive_aloee_ids)
    sql = f"UPDATE {TABLE} SET Ativo='N' WHERE IdProdutoAloee NOT IN ({placeholders})"
    cur = conn.cursor()
    cur.execute(sql, alive_aloee_ids)
    return cur.rowcount
