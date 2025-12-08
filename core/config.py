# core/config.py
from dotenv import load_dotenv
import os

load_dotenv()

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
