from db.connection import get_connection
from utils.logger import log_info

def teste_conexao():
    try:
        conn = get_connection()
        log_info("Conexão com banco estabelecida com sucesso!")
        cursor = conn.cursor()

        # Teste produtos
        cursor.execute("SELECT TOP 5 * FROM Produto")
        produtos = cursor.fetchall()
        log_info(f"Produtos encontrados: {len(produtos)}")
        for p in produtos:
            log_info(f" - {p}")

        # Teste modelos de produção
        cursor.execute("SELECT TOP 5 * FROM ModeloOrdem")
        modelos = cursor.fetchall()
        log_info(f"Modelos de produção encontrados: {len(modelos)}")
        for m in modelos:
            log_info(f" - {m}")

    except Exception as e:
        log_info(f"Erro no teste: {e}")
    finally:
        try:
            conn.close()
            log_info("Conexão encerrada.")
        except:
            pass

if __name__ == "__main__":
    teste_conexao()
