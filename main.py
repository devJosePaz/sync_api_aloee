import traceback
import time
from core.db import get_connection
from core.logger import log_info, write_summary, print_header
from jobs.produto_job import run_produto_job
from jobs.modelo_producao_job import run_modelo_producao_job

def countdown_close(seconds=5):
    print("\n")
    for i in range(seconds, 0, -1):
        print(f"Fechando o console em {i}...", end="\r", flush=True)
        time.sleep(1)
    print("Fechando o console... ✔ ")

def main():
    print_header()
    conn = None
    metrics = {}
    try:
        conn = get_connection()
        log_info("Conexão com banco estabelecida", "info")

        # PRODUTOS
        produto_res = run_produto_job(conn)
        metrics["Produtos"] = {
            "total": produto_res.get("total", 0),
            "inseridos": produto_res.get("inseridos", 0),
            "atualizados": produto_res.get("atualizados", 0),
            "inativados": produto_res.get("inativados", 0)
        }
        map_prod_api_to_id = produto_res.get("map_prod_api_to_id", {})

        # MODELOS DE PRODUÇÃO
        modelo_res = run_modelo_producao_job(conn, map_prod_api_to_id)
        metrics["ModelosProducao"] = {
            "total": modelo_res.get("total", 0),
            "inseridos": modelo_res.get("inseridos", 0),
            "atualizados": modelo_res.get("atualizados", 0),
            "inativados": modelo_res.get("inativados", 0)
        }

        conn.commit()
        log_info("Commit finalizado com sucesso", "info")
        log_info("Sincronização concluída", "info")

        write_summary(metrics)
        countdown_close(3)

    except Exception as e:
        log_info(f"ERRO GERAL: {e}", "error")
        log_info(traceback.format_exc(), "error")
        try:
            if conn:
                conn.rollback()
                log_info("Rollback executado com sucesso", "warning")
        except Exception:
            log_info("Falha ao executar rollback", "error")
        finally:
            try:
                if conn:
                    conn.close()
                    log_info("Conexão encerrada", "info")
            except Exception:
                pass

if __name__ == "__main__":
    main()
