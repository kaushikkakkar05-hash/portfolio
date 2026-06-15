import pyodbc
import pandas as pd

# Connection parameters
server = 'localhost'
database = 'ETL_Project'
driver = 'ODBC Driver 17 for SQL Server'
conn_str = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

try:
    conn = pyodbc.connect(conn_str)
    print("✅ Connected to SQL Server!")

    query = "SELECT * FROM SalesData"
    df = pd.read_sql(query, conn)

    print("📋 Data from SalesData table:")
    print(df)

except Exception as e:
    print("❌ Error:", e)

finally:
    if 'conn' in locals():
        conn.close()
