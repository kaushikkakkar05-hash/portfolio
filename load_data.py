import pyodbc
import pandas as pd

# Sample transformed data (normally comes from previous step)
data = {
    'ProductName': ['Laptop', 'Phone', 'Tablet'],
    'Quantity': [2, 5, 3],
    'Price': [75000.0, 30000.0, 40000.0],
    'SaleDate': ['2025-07-01', '2025-07-02', '2025-07-03'],
    'TotalAmount': [150000.0, 150000.0, 120000.0]
}
df = pd.DataFrame(data)

# Connect to SQL Server
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=KK;'
    'DATABASE=ETL_Project;'
    'Trusted_Connection=yes;'
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    print("✅ Connected to SQL Server!")

    # Drop table if it already exists
    cursor.execute("IF OBJECT_ID('TransformedSalesData', 'U') IS NOT NULL DROP TABLE TransformedSalesData;")
    conn.commit()

    # Create the new table
    cursor.execute("""
        CREATE TABLE TransformedSalesData (
            SaleID INT IDENTITY(1,1) PRIMARY KEY,
            ProductName NVARCHAR(100),
            Quantity INT,
            Price DECIMAL(10, 2),
            SaleDate DATE,
            TotalAmount DECIMAL(18, 2)
        );
    """)
    conn.commit()
    print("🧱 Table TransformedSalesData created.")

    # Insert data
    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO TransformedSalesData (ProductName, Quantity, Price, SaleDate, TotalAmount)
            VALUES (?, ?, ?, ?, ?);
        """, row['ProductName'], row['Quantity'], row['Price'], row['SaleDate'], row['TotalAmount'])
    conn.commit()
    print("📦 Data loaded successfully into TransformedSalesData!")

except Exception as e:
    print("❌ Error:", e)
finally:
    if 'conn' in locals():
        conn.close()
