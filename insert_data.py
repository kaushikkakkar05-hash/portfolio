import pyodbc

# Define the connection string
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=KK;"  # Use your correct server name
    "Database=ETL_Project;"
    "Trusted_Connection=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Sample data to insert
    sales_data = [
        ('Laptop', 2, 75000.00, '2025-07-01'),
        ('Phone', 5, 30000.00, '2025-07-02'),
        ('Tablet', 3, 40000.00, '2025-07-03'),
    ]

    for item in sales_data:
        cursor.execute(
            "INSERT INTO SalesData (ProductName, Quantity, Price, SaleDate) VALUES (?, ?, ?, ?)",
            item
        )

    conn.commit()
    print(" Data inserted successfully!")

except Exception as e:
    print(" Error:", e)

finally:
    conn.close()
