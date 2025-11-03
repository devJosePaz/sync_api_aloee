# config.py

import os
import sys
from dotenv import load_dotenv

# Detecta se está rodando via PyInstaller
if hasattr(sys, "_MEIPASS"):
    env_path = os.path.join(sys._MEIPASS, ".env")
else:
    env_path = ".env"

# Carrega variáveis do .env
load_dotenv(dotenv_path=env_path)

# --- Configuração da API Aloee ---
API_USER = os.getenv("ALOEE_USER")
API_PASSWORD = os.getenv("ALOEE_PASS")
API_BASE_URL = os.getenv("ALOEE_URL", "https://api.aloee.it")

# --- Tipo de banco ---
DB_TYPE = os.getenv("DB_TYPE", "mssql")

# --- SQL Server ---
MSSQL_SERVER = os.getenv("MSSQL_SERVER")
MSSQL_DATABASE = os.getenv("MSSQL_DATABASE")
MSSQL_USER = os.getenv("MSSQL_USER")
MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD")
