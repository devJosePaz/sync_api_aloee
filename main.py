import traceback
import time
from core.db import get_connection
from core.logger import log_info, write_summary, print_header

from jobs.produto_job import run_produto_job
from jobs.modelo_producao_job import run_modelo_producao_job
from jobs.ordem_producao_job import run_ordem_producao_job
from jobs.grupo_recurso_job import run_grupo_recurso_job
from jobs.ordem_operacao_job import run_ordem_operacao_job


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

        # ----------------------------
        # PRODUTOS
        # ----------------------------
        produto_res = run_produto_job(conn)
        metrics["Produtos"] = {
            "total": produto_res.get("total", 0),
            "inseridos": produto_res.get("inseridos", 0),
            "atualizados": produto_res.get("atualizados", 0),
            "inativados": produto_res.get("inativados", 0)
        }
        map_prod_api_to_id = produto_res.get("map_prod_api_to_id", {})

        # ----------------------------
        # MODELOS DE PRODUÇÃO
        # ----------------------------
        modelo_res = run_modelo_producao_job(conn, map_prod_api_to_id)
        metrics["ModelosProducao"] = {
            "total": modelo_res.get("total", 0),
            "inseridos": modelo_res.get("inseridos", 0),
            "atualizados": modelo_res.get("atualizados", 0),
            "inativados": modelo_res.get("inativados", 0)
        }

        # ----------------------------
        # ORDENS DE PRODUÇÃO
        # ----------------------------
        ordem_res = run_ordem_producao_job(conn, map_prod_api_to_id) 
        metrics["OrdensProducao"] = {
            "total": ordem_res.get("total", 0),
            "inseridos": ordem_res.get("inseridos", 0),
            "atualizados": ordem_res.get("atualizados", 0),
            "inativados": ordem_res.get("inativados", 0)
        }
        # mapa correto de ordens para o job de operação
        map_ordem_api_to_id = ordem_res.get("map_api_to_id", {})

        # ----------------------------
        # GRUPO DE RECURSO
        # ----------------------------
        grupo_res = run_grupo_recurso_job(conn)
        metrics["GrupoRecurso"] = {
            "total": grupo_res.get("total", 0),
            "inseridos": grupo_res.get("inseridos", 0),
            "atualizados": grupo_res.get("atualizados", 0),
            "inativados": grupo_res.get("inativados", 0)
        }

        # ----------------------------
        # ORDENS DE OPERAÇÃO
        # ----------------------------
        ordem_ope_res = run_ordem_operacao_job(conn, map_ordem_api_to_id)
        metrics["OrdensOperacao"] = {
            "total": ordem_ope_res.get("total", 0),
            "inseridos": ordem_ope_res.get("inseridos", 0),
            "atualizados": ordem_ope_res.get("atualizados", 0),
            "inativados": ordem_ope_res.get("inativados", 0)
        }

        # ----------------------------
        # COMMIT FINAL
        # ----------------------------
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
