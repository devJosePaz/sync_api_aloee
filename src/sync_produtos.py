from api.endpoints.produto import fetch_products
from services.produto_mapper import map_produto
from repositories.produto_repository import ProdutoRepository
from core.logger import log

def sync_produtos():
    log.info("Iniciando sincronização de produtos...")

    repo = ProdutoRepository()
    dados = fetch_products()

    if not dados:
        log.warning("Nenhum produto retornado da API.")
        return

    for item in dados:
        try:
            produto = map_produto(item)
            repo.upsert(produto)
        except Exception as e:
            log.error(f"Erro ao processar produto {item.get('id')}: {e}")

    log.info("Sincronização de produtos finalizada!")
