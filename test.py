# test.py
from core.db import get_connection
from api.endpoints.ordem_operacao import fetch_ordem_operacao_api
from repositories.ordem_operacao_repository import fetch_all_ordem_operacao
from repositories.ordem_producao_repository import fetch_all_ordens
from services.ordem_operacao_service import sync_ordem_operacao

ops = fetch_ordem_operacao_api()
print(ops[0])
