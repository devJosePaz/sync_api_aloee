from core.db import get_connection

TABLE = "Al_ModeloOrdem"

def fetch_all_modelos_producao(conn):
    """
    Retorna {IdModeloOrdemAloee: {...}} dos modelos de produção no banco.
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

def insert_modelo_producao(conn, item):
    cur = conn.cursor()
    cur.execute(f"""
        INSERT INTO {TABLE} (
            IdModeloOrdemAloee,
            IdProdutoAloee,
            IdProduto,
            Descricao,
            Cliente,
            Quantidade,
            Observacoes,
            Ativo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item.get("id_aloee"),
        item.get("id_produto_aloee"),
        item.get("id_produto"),
        item.get("descricao"),
        item.get("cliente"),
        item.get("quantidade"),
        item.get("observacoes"),
        "S"
    ))
    cur.execute("SELECT SCOPE_IDENTITY()")
    return cur.fetchone()[0]

def update_modelo_producao(conn, item):
    cur = conn.cursor()
    cur.execute(f"""
        UPDATE {TABLE}
        SET
            IdProdutoAloee = ?,
            IdProduto = ?,
            Descricao = ?,
            Cliente = ?,
            Quantidade = ?,
            Observacoes = ?,
            Ativo = ?
        WHERE IdModeloOrdemAloee = ?
    """, (
        item.get("id_produto_aloee"),
        item.get("id_produto"),
        item.get("descricao"),
        item.get("cliente"),
        item.get("quantidade"),
        item.get("observacoes"),
        "S",
        item.get("id_aloee")
    ))
    return cur.rowcount

def mark_inactive_missing_modelo_producao(conn, alive_ids: list):
    if not alive_ids:
        return 0
    placeholders = ",".join("?" for _ in alive_ids)
    sql = f"UPDATE {TABLE} SET Ativo='N' WHERE IdModeloOrdemAloee NOT IN ({placeholders})"
    cur = conn.cursor()
    cur.execute(sql, alive_ids)
    return cur.rowcount
