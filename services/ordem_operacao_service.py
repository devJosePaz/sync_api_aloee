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
    existentes = fetch_all_ordens_operacao(conn)

    total = 0
    inseridos = 0
    atualizados = 0

    for item in itens_api:
        total += 1

        # 🔴 CHAVES CORRETAS — iguais às do endpoint
        uuid_op = item.get("id_ordem_producao_ope_aloee")
        uuid_ordem = item.get("id_ordem_producao_aloee")
        uuid_grupo = item.get("id_grupo_recurso_aloee")

        if not uuid_op or not uuid_ordem or not uuid_grupo:
            log_info(
                f"Pulando OrdemOperacao — IDs inválidos: "
                f"op={uuid_op}, ordem={uuid_ordem}, grupo={uuid_grupo}",
                "warning",
            )
            continue

        ordem = map_ordem_producao.get(uuid_ordem)
        grupo = map_grupo_recurso.get(uuid_grupo)

        if not ordem or not grupo:
            log_info(
                f"Pulando OrdemOperacao {uuid_op} — FK não resolvida",
                "warning",
            )
            continue

        payload = {
            "IdOrdemProducaoOpeAloee": uuid_op,
            "IdOrdemProducao": ordem["IdOrdemProducao"],
            "IdOrdemProducaoAloee": uuid_ordem,
            "IdGrupoRecurso": grupo["IdGrupoRecurso"],
            "IdGrupoRecursoAloee": uuid_grupo,
            "Ativo": "S",
        }

        for campo_sql, campo_api in MAP_CAMPO_ITEM.items():
            payload[campo_sql] = item.get(campo_api)

        existente = existentes.get(uuid_op)

        if not existente:
            insert_ordem_operacao(conn, payload)
            inseridos += 1
            log_info(f"Inserida OrdemOperacao {uuid_op}", "info")
            continue

        diff = {}
        for campo in MAP_CAMPO_ITEM.keys():
            if existente.get(campo) != payload.get(campo):
                diff[campo] = payload[campo]

        if diff:
            update_ordem_operacao(
                conn,
                existente["IdOrdemProducaoOpe"],
                diff,
            )
            atualizados += 1
            log_info(
                f"Atualizada OrdemOperacao {uuid_op} — {list(diff.keys())}",
                "info",
            )

    # 🔵 RETORNO OBRIGATÓRIO PRO JOB / MAIN
    return {
        "total": total,
        "inseridos": inseridos,
        "atualizados": atualizados,
        "inativados": 0,
    }
