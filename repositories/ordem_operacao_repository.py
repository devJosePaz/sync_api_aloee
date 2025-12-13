# repositories/ordem_operacao_repository.py

TABLE = "Al_OrdemOperacao"


def fetch_all_ordens_operacao(conn):
    """
    Retorna todas as ordens de operação indexadas pelo UUID Aloee
    (UUID é apenas referência externa, NÃO FK)
    """
    query = f"""
        SELECT *
        FROM {TABLE}
    """

    cursor = conn.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]

    resultado = {}
    for row in rows:
        data = dict(zip(columns, row))
        resultado[data["IdOrdemProducaoOpeAloee"]] = data

    return resultado


def insert_ordem_operacao(conn, dados):
    """
    Insere uma ordem de operação.
    Commit é controlado pelo main.
    """
    cols = ", ".join(dados.keys())
    placeholders = ", ".join(["?"] * len(dados))

    query = f"""
        INSERT INTO {TABLE} ({cols})
        VALUES ({placeholders})
    """

    cursor = conn.cursor()
    cursor.execute(query, list(dados.values()))


def update_ordem_operacao(conn, id_interno, dados):
    """
    Atualiza uma ordem de operação pelo ID interno (INT IDENTITY).
    """
    sets = ", ".join([f"{k} = ?" for k in dados.keys()])

    query = f"""
        UPDATE {TABLE}
        SET {sets}
        WHERE IdOrdemProducaoOpe = ?
    """

    cursor = conn.cursor()
    cursor.execute(query, list(dados.values()) + [id_interno])
