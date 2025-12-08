import sys
import traceback

from core.logger import print_header, log_info, write_summary
from core.config import load_env

# IMPORTAR CADA SYNC AQUI
from services.sync_produtos import sync_produtos
# from services.sync_modelos import sync_modelos
# from services.sync_turnos import sync_turnos
# ...
# (quando for criando os próximos, é só ir adicionando)


def main():
    print_header()
    load_env()

    log_info("Iniciando processo geral de sincronização...", "info")

    metrics = {}

    try:
        # ========================
        # EXECUÇÃO SEQUENCIAL
        # ========================
        
        log_info("Sincronizando produtos...")
        metrics["Produtos"] = sync_produtos()

        # log_info("Sincronizando modelos...")
        # metrics["Modelos"] = sync_modelos()

        # log_info("Sincronizando turnos...")
        # metrics["Turnos"] = sync_turnos()

        # ...
        # (adicione conforme criar os módulos)

    except Exception as e:
        log_info(f"Erro crítico durante sincronização: {str(e)}", "error")
        traceback.print_exc()

    finally:
        log_info("Finalizando execução...", "info")
        write_summary(metrics)
        log_info("Processo concluído.\n", "info")


if __name__ == "__main__":
    main()
