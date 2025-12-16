from core.db import get_connection

TABLE = "Al_Produto"

def fetch_all_produtos(conn):
    """
    Retorna dict {IdProdutoAloee: {...}} com:
    IdProduto, IdProdutoAloee, Descricao, Unidade, Dependencia (IdProduto interno), Ativo
    """
    cur = conn.cursor()
    cur.execute(f"""
        SELECT IdProduto, IdProdutoAloee, Descricao, Unidade, IdProdutoDep, Ativo
        FROM {TABLE}
    """)
    rows = cur.fetchall()
    result = {}
    for r in rows:
        result[str(r[1])] = {
            "IdProduto": r[0],
            "IdProdutoAloee": r[1],
            "Descricao": r[2],
            "Unidade": r[3],
            "Dependencia": r[4],  # IdProduto interno
            "Ativo": r[5]
        }
    return result

def get_produto_by_aloee(conn, id_aloee):
    cur = conn.cursor()
    cur.execute(f"SELECT IdProduto FROM {TABLE} WHERE IdProdutoAloee = ?", id_aloee)
    row = cur.fetchone()
    return row[0] if row else None

def insert_produto(conn, item, map_prod_api_to_id):
    """
    Insere produto. Usa IdProduto interno da dependência se existir.
    """
    dep_interno = map_prod_api_to_id.get(item.get("dependencia_id_aloee"))
    cur = conn.cursor()
    cur.execute(f"""
        INSERT INTO {TABLE} (
            IdProdutoAloee,
            IdProdutoDep,
            CodMaterial,
            Descricao,
            Unidade,
            Ativo
        ) VALUES (?, ?, NULL, ?, ?, ?)
    """, (
        item.get("id_aloee"),
        dep_interno,  # Pode ser None se dependência ainda não existir
        item.get("descricao"),
        item.get("unidade"),
        'S'
    ))
    cur.execute("SELECT SCOPE_IDENTITY()")
    return cur.fetchone()[0]

def update_produto(conn, item, map_prod_api_to_id):
    """
    Atualiza produto. Usa IdProduto interno da dependência se existir.
    """
    dep_interno = map_prod_api_to_id.get(item.get("dependencia_id_aloee"))
    cur = conn.cursor()
    cur.execute(f"""
        UPDATE {TABLE}
        SET
            IdProdutoDep = ?,
            Descricao = ?,
            Unidade = ?,
            Ativo = ?
        WHERE IdProdutoAloee = ?
    """, (
        dep_interno,
        item.get("descricao"),
        item.get("unidade"),
        'S',
        item.get("id_aloee")
    ))
    return cur.rowcount

def mark_inactive_missing(conn, alive_aloee_ids: list):
    """
    Marca produtos que não estão mais na API como inativos.
    """
    if not alive_aloee_ids:
        return 0
    placeholders = ",".join("?" for _ in alive_aloee_ids)
    sql = f"UPDATE {TABLE} SET Ativo='N' WHERE IdProdutoAloee NOT IN ({placeholders})"
    cur = conn.cursor()
    cur.execute(sql, alive_aloee_ids)
    return cur.rowcount
