import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=10.1.2.8,53546;"  # substitua pelo IP real do servidor
    "DATABASE=ProgetQuimAtu;"
    "UID=PROMICRO;"
    "PWD=AQUARELA;"
    "TrustServerCertificate=yes;"
    "Network=DBMSSOCN;"  # força TCP/IP
)

try:
    conn = pyodbc.connect(conn_str, autocommit=False, timeout=10)
    print("Conexão OK")
except pyodbc.Error as e:
    print("Erro:", e)
