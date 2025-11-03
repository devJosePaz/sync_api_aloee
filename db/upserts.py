# db/upserts.py

def upsert_product(conn, product):
    """
    Upsert para Produto.
    product keys: id (IdProdAloee da API), name, previous_dependency, unit
    Retorna o IdProduto interno (int).
    """
    cursor = conn.cursor()
    cursor.execute("SELECT IdProduto FROM Produto WHERE IdProdAloee=?", (product["id"],))
    row = cursor.fetchone()

    if row:
        # Atualiza dados e marca como ativo
        cursor.execute("""
            UPDATE Produto
            SET Nome=?, Dependencia=?, Unidade=?, Ativo='S'
            WHERE IdProdAloee=?
        """, (product["name"], product.get("previous_dependency"), product.get("unit"), product["id"]))
        return row[0]
    else:
        # Insere novo produto e pega o IdProduto gerado
        cursor.execute("""
            INSERT INTO Produto (IdProdAloee, Nome, Dependencia, Unidade, Ativo)
            OUTPUT INSERTED.IdProduto
            VALUES (?, ?, ?, ?, 'S')
        """, (product["id"], product["name"], product.get("previous_dependency"), product.get("unit")))
        new_id = cursor.fetchone()[0]
        return new_id


def upsert_model(conn, model):
    """
    Upsert para Modelo de Produção.
    model keys: id (IdModeloAloee), name, product_id (IdProduto interno), product_api_id (IdProdAloee da API), quantidade
    """
    cursor = conn.cursor()
    # Verifica se já existe pelo IdModeloAloee
    cursor.execute("SELECT COUNT(*) FROM ModeloOrdem WHERE IdModeloAloee=?", (model["id"],))
    exists = cursor.fetchone()[0]

    if exists:
        # Atualiza dados
        cursor.execute("""
            UPDATE ModeloOrdem
            SET Nome=?, IdProduto=?, IdProdAloee=?, Quantidade=?, Ativo='S'
            WHERE IdModeloAloee=?
        """, (
            model["name"],
            model.get("product_id"),   # <-- ID interno (int)
            model.get("product_api_id"),  # <-- ID da API (nvarchar)
            model.get("quantidade", 0),
            model["id"]
        ))
    else:
        # Insere novo modelo
        cursor.execute("""
            INSERT INTO ModeloOrdem (IdModeloAloee, Nome, IdProduto, IdProdAloee, Quantidade, Ativo)
            OUTPUT INSERTED.IdModOrd
            VALUES (?, ?, ?, ?, ?, 'S')
        """, (
            model["id"],
            model["name"],
            model.get("product_id"),      # <-- ID interno (int)
            model.get("product_api_id"),  # <-- ID da API (nvarchar)
            model.get("quantidade", 0)
        ))
        # Pega o ID interno recém-criado
        id_modord = cursor.fetchone()[0]
        conn.commit()
        return id_modord
