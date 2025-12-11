# repositories/grupo_recurso_repository.py
from core.db import get_connection

TABLE = "Al_GrupoRecurso"


def fetch_all_grupos(conn):
    cur = conn.cursor()
    cur.execute(f"""
        SELECT
            IdGrupoRecurso,
            IdGrupoRecursoAloee,
            IdCalendario,
            IdCalendarioAloee,
            Descricao,
            Restricao,
            Unidade,
            Quantidade,
            Maximo,
            LimitesOee,
            LimiteA,
            LimiteB,
            Ativo
        FROM {TABLE}
    """)
    rows = cur.fetchall()

    result = {}
    for r in rows:
        result[str(r[1])] = {
            "IdGrupoRecurso": r[0],
            "IdGrupoRecursoAloee": r[1],
            "IdCalendario": r[2],
            "IdCalendarioAloee": r[3],
            "Descricao": r[4],
            "Restricao": r[5],
            "Unidade": r[6],
            "Quantidade": r[7],
            "Maximo": r[8],
            "LimitesOee": r[9],
            "LimiteA": r[10],
            "LimiteB": r[11],
            "Ativo": r[12]
        }
    return result


def insert_grupo(conn, item):
    cur = conn.cursor()
    cur.execute(f"""
        INSERT INTO {TABLE} (
            IdGrupoRecursoAloee,
            IdCalendario,
            IdCalendarioAloee,
            Descricao,
            Restricao,
            Unidade,
            Quantidade,
            Maximo,
            LimitesOee,
            LimiteA,
            LimiteB,
            Ativo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item.get("id_aloee"),
        item.get("id_calendario"),
        item.get("id_calendario_aloee"),
        item.get("descricao"),
        item.get("restricao"),
        item.get("unidade"),
        item.get("quantidade"),
        item.get("maximo"),
        item.get("limites_oee"),
        item.get("limite_a"),
        item.get("limite_b"),
        'S'
    ))

    # Retorna o último ID criado
    cur.execute(f"SELECT TOP 1 IdGrupoRecurso FROM {TABLE} ORDER BY IdGrupoRecurso DESC")
    return cur.fetchone()[0]


def update_grupo(conn, item):
    cur = conn.cursor()
    cur.execute(f"""
        UPDATE {TABLE}
        SET
            IdCalendario = ?,
            IdCalendarioAloee = ?,
            Descricao = ?,
            Restricao = ?,
            Unidade = ?,
            Quantidade = ?,
            Maximo = ?,
            LimitesOee = ?,
            LimiteA = ?,
            LimiteB = ?,
            Ativo = ?
        WHERE IdGrupoRecursoAloee = ?
    """, (
        item.get("id_calendario"),
        item.get("id_calendario_aloee"),
        item.get("descricao"),
        item.get("restricao"),
        item.get("unidade"),
        item.get("quantidade"),
        item.get("maximo"),
        item.get("limites_oee"),
        item.get("limite_a"),
        item.get("limite_b"),
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
        f"UPDATE {TABLE} SET Ativo='N' WHERE IdGrupoRecursoAloee NOT IN ({placeholders})",
        alive_aloee_ids
    )
    return cur.rowcount
