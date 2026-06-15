import pyodbc
import pandas as pd

# Connect to SQL Server
server = 'localhost'
database = 'ETL_Project'
driver = 'ODBC Driver 17 for SQL Server'
conn_str = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

try:
    conn = pyodbc.connect(conn_str)
    print("✅ Connected to SQL Server!")

    # Read data from SalesData
    query = "SELECT * FROM SalesData"
    df = pd.read_sql(query, conn)

    # Transformation: Add TotalAmount column
    df['TotalAmount'] = df['Quantity'] * df['Price']

    print("\n🔁 Transformed Data:")
    print(df)

except Exception as e:
    print("❌ Error:", e)

finally:
    if 'conn' in locals():
        conn.close()
