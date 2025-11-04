import traceback
from db.connection import get_connection
from utils.logger import log_info, write_summary, print_header
from process.produtos_process import process_produtos
from process.modelos_process import process_modelos
import time

def countdown_close(seconds=5):
    """Contagem regressiva antes de fechar o console"""
    print("\n")
    for i in range(seconds, 0, -1):
        print(f"Fechando o console em {i}...", end="\r", flush=True)
        time.sleep(1)
    print("Fechando o console... ✔ ")

def main():
    print_header()
    try:
        conn = get_connection()
        log_info("Conexão com banco estabelecida", status="info")

        # Processa produtos
        produtos_total, produtos_inseridos, produtos_atualizados, map_prod_api_to_id = process_produtos(conn)

        # Processa modelos
        modelos_total, modelos_inseridos, modelos_atualizados = process_modelos(conn, map_prod_api_to_id)

        conn.commit()
        log_info("Commit finalizado com sucesso", status="info")
        log_info("Sincronização concluída", status="info")

        # Resumo final
        write_summary(
            produtos_total=produtos_total,
            produtos_inseridos=produtos_inseridos,
            produtos_atualizados=produtos_atualizados,
            modelos_total=modelos_total,
            modelos_inseridos=modelos_inseridos,
            modelos_atualizados=modelos_atualizados
        )

        countdown_close(3)

    except Exception as e:
        log_info(f"ERRO GERAL: {e}", status="error")
        log_info(traceback.format_exc(), status="error")
        try:
            conn.rollback()
            log_info("Rollback executado com sucesso", status="warning")
        except:
            log_info("Falha ao executar rollback", status="error")
        finally:
            try:
                conn.close()
                log_info("Conexão encerrada", status="info")
            except:
                pass

if __name__ == "__main__":
    main()
