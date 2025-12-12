# api/endpoints/ordem_operacao.py
from api.client import client

def fetch_ordem_operacao_api():
    itens = []
    for page_items in client.paginate("/v1/Operation"):
        for entry in page_items:
            d = entry.get("data", {}) if isinstance(entry, dict) else {}

            itens.append({
                "id_ordem_producao_ope_aloee": d.get("id"),
                "id_ordem_producao_aloee": d.get("productionOrderId"),
                "id_grupo_recurso_aloee": d.get("resourceGroupId"),
                "situacao": d.get("progressStatus"),
                "descricao": d.get("name"),
                "nivel": d.get("operationLevel"),
                "quantidade_variavel": 'S' if d.get("variableQuantity") else 'N',
                "quantidade": d.get("expectedProductionQuantity", 0),
                "unidade": d.get("unit"),
                "tempo_variavel": 'S' if d.get("variableTime") else 'N',
                "tempo_producao": d.get("productionTime", 0),
                "tempo_setup_fixo": d.get("fixedSetupTime"),
                "tempo_setup_variavel": d.get("variableSetupTime"),
                "tempo_max_parada": d.get("maximumStopTime"),
                "tempo_min_proxima": d.get("minimumTimeToNextOperation"),
                "tempo_max_proxima": d.get("maximumTimeToNextOperation"),
                "lote_transferencia": d.get("transferBatchQuantityNextOperation"),
                "observacoes": d.get("notes") or d.get("observation"),
                "data_coleta": d.get("snapshotTime"),
                "qtd_boa": d.get("goodQuantity"),
                "qtd_retrabalho": d.get("reworkQuantity"),
                "qtd_sucata": d.get("scrapQuantity"),
                "qtd_unitaria": d.get("unitQuantity"),
                "tempo_prod_decorrido": d.get("elapsedProductionTime"),
                "tempo_prod_real": d.get("effectiveProductionTime"),
                "tempo_parada_planejado_real": d.get("effectivePlannedStopTime"),
                "tempo_parada_nao_planejado_real": d.get("effectiveUnplannedStopTime"),
                "tempo_setup_real": d.get("effectiveSetupTime"),
            })
    return itens
