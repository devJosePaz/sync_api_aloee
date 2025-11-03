# db/connection.py
import pyodbc
from config import MSSQL_SERVER, MSSQL_DATABASE, MSSQL_USER, MSSQL_PASSWORD

def get_connection():
    """
    Retorna uma conexão ativa com o SQL Server usando ODBC 17.
    """
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={MSSQL_SERVER};"
        f"DATABASE={MSSQL_DATABASE};"
        f"UID={MSSQL_USER};"
        f"PWD={MSSQL_PASSWORD};"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str, autocommit=False)
