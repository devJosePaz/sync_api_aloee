import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ALOEE_USER = os.getenv("ALOEE_USER")
    ALOEE_PASS = os.getenv("ALOEE_PASS")
    ALOEE_URL = os.getenv("ALOEE_URL")

    DB_TYPE = os.getenv("DB_TYPE")

    MSSQL_SERVER = os.getenv("MSSQL_SERVER")
    MSSQL_DATABASE = os.getenv("MSSQL_DATABASE")
    MSSQL_USER = os.getenv("MSSQL_USER")
    MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD")

settings = Settings()
