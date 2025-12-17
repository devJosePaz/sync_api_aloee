from dotenv import load_dotenv
import os
import sys

# Detecta se está rodando dentro do PyInstaller
if getattr(sys, "frozen", False):
    # Quando empacotado em .exe, o PyInstaller coloca arquivos extras em _MEIPASS
    base_path = sys._MEIPASS
else:
    # Rodando normal no Python
    base_path = os.getcwd()  # diretório de onde o terminal é executado

# Caminho do .env
env_path = os.path.join(base_path, ".env")

# Carrega o .env
if not os.path.exists(env_path):
    raise FileNotFoundError(f".env não encontrado em: {env_path}")
load_dotenv(dotenv_path=env_path)

class Settings:
    ALOEE_USER = os.getenv("ALOEE_USER")
    ALOEE_PASS = os.getenv("ALOEE_PASS")
    ALOEE_URL = os.getenv("ALOEE_URL", "https://api.aloee.it")
    PAGE_SIZE = int(os.getenv("PAGE_SIZE", "500"))

    DB_TYPE = os.getenv("DB_TYPE", "mssql")
    MSSQL_SERVER = os.getenv("MSSQL_SERVER")
    MSSQL_DATABASE = os.getenv("MSSQL_DATABASE")
    MSSQL_USER = os.getenv("MSSQL_USER")
    MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD")
    MSSQL_DRIVER = os.getenv("MSSQL_DRIVER", "ODBC Driver 17 for SQL Server")

settings = Settings()
