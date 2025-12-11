#repositories/ordem_operacao_repo.py
from core.db import get_connection

TABLE = "Al_OrdemOperacao"

def fetch_all_ordens(conn):
    """
    Retorna dicionário {IdOrdemProducaoOpeAloee: {...}} com colunas:
    IdOrdemProducaoOpe, IdOrdemProducaoOpeAloee, IdOrdemProducao, IdOrdemProducaoAloee,
    IdGrupoRecurso, IdGrupoRecursoAloee, Situacao, Descricao, Nivel, QuantidadeVariavel,
    Quantidade, Unidade, TempoVariavel, TempoProducao, TempoSetupFixo, TempoSetupVariavel,
    TempoMaxParada, TempoMinProxima, TempoMaxProxima, LoteTransferencia, Observacoes,
    DataColeta, QtdBoa, QtdRetrabalho, QtdSucata, QtdUnitaria, TempoProdDecorrido,
    TempoProdReal, TempoParadaPlanejadoReal, TempoParadaNaoPlanejadoReal, TempoSetupReal, Ativo
    """
    cur = conn.cursor()
    cur.execute(f"""
        SELECT *
        FROM {TABLE}
    """)
    rows = cur.fetchall()
    result = {}
    for r in rows:
        result[str(r[1])] = {
            "IdOrdemProducaoOpe": r[0],
            "IdOrdemProducaoOpeAloee": r[1],
            "IdOrdemProducao": r[2],
            "IdOrdemProducaoAloee": r[3],
            "IdGrupoRecurso": r[4],
            "IdGrupoRecursoAloee": r[5],
            "Situacao": r[6],
            "Descricao": r[7],
            "Nivel": r[8],
            "QuantidadeVariavel": r[9],
            "Quantidade": r[10],
            "Unidade": r[11],
            "TempoVariavel": r[12],
            "TempoProducao": r[13],
            "TempoSetupFixo": r[14],
            "TempoSetupVariavel": r[15],
            "TempoMaxParada": r[16],
            "TempoMinProxima": r[17],
            "TempoMaxProxima": r[18],
            "LoteTransferencia": r[19],
            "Observacoes": r[20],
            "DataColeta": r[21],
            "QtdBoa": r[22],
            "QtdRetrabalho": r[23],
            "QtdSucata": r[24],
            "QtdUnitaria": r[25],
            "TempoProdDecorrido": r[26],
            "TempoProdReal": r[27],
            "TempoParadaPlanejadoReal": r[28],
            "TempoParadaNaoPlanejadoReal": r[29],
            "TempoSetupReal": r[30],
            "Ativo": r[31]
        }
    return result

def get_ordem_by_aloee(conn, id_aloee):
    cur = conn.cursor()
    cur.execute(f"SELECT IdOrdemProducaoOpe FROM {TABLE} WHERE IdOrdemProducaoOpeAloee = ?", id_aloee)
    row = cur.fetchone()
    return row[0] if row else None

def insert_ordem(conn, item, id_ordem_interno, id_grupo_recurso_interno):
    """
    item: dict vindo da API (campos conforme endpoint)
    id_ordem_interno: IdOrdemProducao (int) já resolvido pelo map Aloee -> ID interno
    id_grupo_recurso_interno: IdGrupoRecurso (int) já resolvido pelo map Aloee -> ID interno
    """
    cur = conn.cursor()
    cur.execute(f"""
        INSERT INTO {TABLE} (
            IdOrdemProducaoOpeAloee,
            IdOrdemProducao,
            IdOrdemProducaoAloee,
            IdGrupoRecurso,
            IdGrupoRecursoAloee,
            Situacao,
            Descricao,
            Nivel,
            QuantidadeVariavel,
            Quantidade,
            Unidade,
            TempoVariavel,
            TempoProducao,
            TempoSetupFixo,
            TempoSetupVariavel,
            TempoMaxParada,
            TempoMinProxima,
            TempoMaxProxima,
            LoteTransferencia,
            Observacoes,
            DataColeta,
            QtdBoa,
            QtdRetrabalho,
            QtdSucata,
            QtdUnitaria,
            TempoProdDecorrido,
            TempoProdReal,
            TempoParadaPlanejadoReal,
            TempoParadaNaoPlanejadoReal,
            TempoSetupReal,
            Ativo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item.get("id_ordem_producao_ope_aloee"),
        id_ordem_interno,
        item.get("id_ordem_producao_aloee"),
        id_grupo_recurso_interno,
        item.get("id_grupo_recurso_aloee"),
        item.get("situacao"),
        item.get("descricao"),
        item.get("nivel"),
        item.get("quantidade_variavel"),
        item.get("quantidade"),
        item.get("unidade"),
        item.get("tempo_variavel"),
        item.get("tempo_producao"),
        item.get("tempo_setup_fixo"),
        item.get("tempo_setup_variavel"),
        item.get("tempo_max_parada"),
        item.get("tempo_min_proxima"),
        item.get("tempo_max_proxima"),
        item.get("lote_transferencia"),
        item.get("observacoes"),
        item.get("data_coleta"),
        item.get("qtd_boa"),
        item.get("qtd_retrabalho"),
        item.get("qtd_sucata"),
        item.get("qtd_unitaria"),
        item.get("tempo_prod_decorrido"),
        item.get("tempo_prod_real"),
        item.get("tempo_parada_planejado_real"),
        item.get("tempo_parada_nao_planejado_real"),
        item.get("tempo_setup_real"),
        'S'
    ))
    cur.execute("SELECT SCOPE_IDENTITY()")
    return cur.fetchone()[0]

def update_ordem(conn, item, id_ordem_interno, id_grupo_recurso_interno):
    cur = conn.cursor()
    cur.execute(f"""
        UPDATE {TABLE}
        SET
            IdOrdemProducao = ?,
            IdOrdemProducaoAloee = ?,
            IdGrupoRecurso = ?,
            IdGrupoRecursoAloee = ?,
            Situacao = ?,
            Descricao = ?,
            Nivel = ?,
            QuantidadeVariavel = ?,
            Quantidade = ?,
            Unidade = ?,
            TempoVariavel = ?,
            TempoProducao = ?,
            TempoSetupFixo = ?,
            TempoSetupVariavel = ?,
            TempoMaxParada = ?,
            TempoMinProxima = ?,
            TempoMaxProxima = ?,
            LoteTransferencia = ?,
            Observacoes = ?,
            DataColeta = ?,
            QtdBoa = ?,
            QtdRetrabalho = ?,
            QtdSucata = ?,
            QtdUnitaria = ?,
            TempoProdDecorrido = ?,
            TempoProdReal = ?,
            TempoParadaPlanejadoReal = ?,
            TempoParadaNaoPlanejadoReal = ?,
            TempoSetupReal = ?,
            Ativo = ?
        WHERE IdOrdemProducaoOpeAloee = ?
    """, (
        id_ordem_interno,
        item.get("id_ordem_producao_aloee"),
        id_grupo_recurso_interno,
        item.get("id_grupo_recurso_aloee"),
        item.get("situacao"),
        item.get("descricao"),
        item.get("nivel"),
        item.get("quantidade_variavel"),
        item.get("quantidade"),
        item.get("unidade"),
        item.get("tempo_variavel"),
        item.get("tempo_producao"),
        item.get("tempo_setup_fixo"),
        item.get("tempo_setup_variavel"),
        item.get("tempo_max_parada"),
        item.get("tempo_min_proxima"),
        item.get("tempo_max_proxima"),
        item.get("lote_transferencia"),
        item.get("observacoes"),
        item.get("data_coleta"),
        item.get("qtd_boa"),
        item.get("qtd_retrabalho"),
        item.get("qtd_sucata"),
        item.get("qtd_unitaria"),
        item.get("tempo_prod_decorrido"),
        item.get("tempo_prod_real"),
        item.get("tempo_parada_planejado_real"),
        item.get("tempo_parada_nao_planejado_real"),
        item.get("tempo_setup_real"),
        'S',
        item.get("id_ordem_producao_ope_aloee")
    ))
    return cur.rowcount

def mark_inactive_missing(conn, alive_aloee_ids: list):
    """
    Marca como Ativo='N' todos registros cujo IdOrdemProducaoOpeAloee nao estiver na lista alive_aloee_ids.
    """
    if not alive_aloee_ids:
        return 0
    placeholders = ",".join("?" for _ in alive_aloee_ids)
    sql = f"UPDATE {TABLE} SET Ativo='N' WHERE IdOrdemProducaoOpeAloee NOT IN ({placeholders})"
    cur = conn.cursor()
    cur.execute(sql, alive_aloee_ids)
    return cur.rowcount

