from repositories.ordem_operacao_repository import (
    fetch_all_ordens_operacao,
    insert_ordem_operacao,
    update_ordem_operacao,
)
from core.logger import log_info

MAP_CAMPO_ITEM = {
    "Situacao": "situacao",
    "Descricao": "descricao",
    "Nivel": "nivel",
    "QuantidadeVariavel": "quantidade_variavel",
    "Quantidade": "quantidade",
    "Unidade": "unidade",
    "TempoVariavel": "tempo_variavel",
    "TempoProducao": "tempo_producao",
    "TempoSetupFixo": "tempo_setup_fixo",
    "TempoSetupVariavel": "tempo_setup_variavel",
    "TempoMaxParada": "tempo_max_parada",
    "TempoMinProxima": "tempo_min_proxima",
    "TempoMaxProxima": "tempo_max_proxima",
    "LoteTransferencia": "lote_transferencia",
    "Observacoes": "observacoes",
    "DataColeta": "data_coleta",
    "QtdBoa": "qtd_boa",
    "QtdRetrabalho": "qtd_retrabalho",
    "QtdSucata": "qtd_sucata",
    "QtdUnitaria": "qtd_unitaria",
    "TempoProdDecorrido": "tempo_prod_decorrido",
    "TempoProdReal": "tempo_prod_real",
    "TempoParadaPlanejadoReal": "tempo_parada_planejado_real",
    "TempoParadaNaoPlanejadoReal": "tempo_parada_nao_planejado_real",
    "TempoSetupReal": "tempo_setup_real",
}


def sync_ordens_operacao(
    conn,
    itens_api,
    map_ordem_producao,
    map_grupo_recurso,
):
    """
    Sincroniza Ordens de Operação.
    - Resolve FKs exclusivamente via mapas internos
    - Nunca insere FK inválida
    - UUID Aloee é apenas referência externa
    """

    existentes = fetch_all_ordens_operacao(conn)

    total = 0
    inseridos = 0
    atualizados = 0
    ignorados = 0

    for item in itens_api:
        total += 1

        uuid_op = item.get("id_ordem_producao_ope_aloee")
        uuid_ordem = item.get("id_ordem_producao_aloee")
        uuid_grupo = item.get("id_grupo_recurso_aloee")

        # 🔑 RESOLUÇÃO DAS FKs (OBRIGATÓRIA)
        ordem_row = map_ordem_producao.get(uuid_ordem)
        grupo_row = map_grupo_recurso.get(uuid_grupo)

        nome_ordem = ordem_row.get("Descricao") if ordem_row else None
        nome_grupo = grupo_row.get("Descricao") if grupo_row else None

        if not ordem_row:
            log_info(
                f"[IGNORADO] OrdemOperacao {uuid_op} — OrdemProducao não encontrada (UUID={uuid_ordem})",
                "warning",
            )
            ignorados += 1
            continue

        if not grupo_row:
            log_info(
                f"[IGNORADO] OrdemOperacao {uuid_op} — GrupoRecurso não encontrado (UUID={uuid_grupo})",
                "warning",
            )
            ignorados += 1
            continue

        id_ordem = ordem_row["IdOrdemProducao"]
        id_grupo = grupo_row["IdGrupoRecurso"]

        payload = {
            "IdOrdemProducaoOpeAloee": uuid_op,
            "IdOrdemProducao": id_ordem,
            "IdGrupoRecurso": id_grupo,
            "IdOrdemProducaoAloee": uuid_ordem,
            "IdGrupoRecursoAloee": uuid_grupo,
            "Ativo": "S",
        }

        for campo_sql, campo_api in MAP_CAMPO_ITEM.items():
            payload[campo_sql] = item.get(campo_api)

        existente = existentes.get(uuid_op)

        # -----------------------
        # INSERT
        # -----------------------
        if not existente:
            insert_ordem_operacao(conn, payload)
            inseridos += 1
            log_info(f"Inserida OrdemOperacao {nome_ordem} / {nome_grupo} ({uuid_op})", "info")
            continue

        # -----------------------
        # UPDATE (DIFF)
        # -----------------------
        diff = {}
        for campo, valor in payload.items():
            if existente.get(campo) != valor:
                diff[campo] = valor

        if diff:
            update_ordem_operacao(conn, existente["IdOrdemProducaoOpe"], diff)
            atualizados += 1
            log_info(
                f"Atualizada OrdemOperacao {nome_ordem} / {nome_grupo} ({uuid_op}) — campos: {list(diff.keys())}",
                "info",
            )

    return {
        "total": total,
        "inseridos": inseridos,
        "atualizados": atualizados,
        "ignorados": ignorados,
        "inativados": 0,
    }
