import pyodbc
from core.config import settings

def get_connection():
    """
    Retorna conexão pyodbc (autocommit False).
    """
    conn_str = (
        f"DRIVER={{{settings.MSSQL_DRIVER}}};"
        f"SERVER={settings.MSSQL_SERVER};"
        f"DATABASE={settings.MSSQL_DATABASE};"
        f"UID={settings.MSSQL_USER};"
        f"PWD={settings.MSSQL_PASSWORD};"
        "TrustServerCertificate=yes;"
        "Network=DBMSSOCN;"  # força TCP/IP
    )
    return pyodbc.connect(conn_str, autocommit=False)
