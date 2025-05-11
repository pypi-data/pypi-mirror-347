# 📌 PyDBManager - SQL Server Database Manager  

![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)  ![SQL Server](https://img.shields.io/badge/SQL%20Server-ODBC%20Driver%2017-red.svg)  ![MIT License](https://img.shields.io/badge/License-MIT-green.svg)  

Welcome to **PyDBManager** – a Python package for managing **SQL Server connections and queries** easily and efficiently! 🌟  

This guide will help you:
- ✅ Install PyDBManager
- ✅ Set up your `.env` file for SQL or Windows Authentication
- ✅ Perform SQL operations using Python
- ✅ Create tables, insert, update, and bulk load DataFrames
- ✅ Save query results and use batch fetching

---

## **1. Install PyDBManager**  
Run the following command to install `PyDBManager`:
```bash
pip install pydbmanager
```
**If installation is successful, continue to the next step!**  

---

## **2. Create `.env` File to Store Database Credentials**  
To avoid hardcoding credentials, create a `.env` file in your project directory.

### **Steps**  
1. **Create a `.env` file** in your project root.  
2. **Add the following credentials** (update as needed):
    ```env
    DB_SERVER=localhost
    DB_DATABASE=your_database_name
    DB_DRIVER=ODBC Driver 17 for SQL Server

    # For SQL Authentication
    DB_USERNAME=your_username
    DB_PASSWORD=your_password
    DB_AUTH_MODE=sql

    # For Windows Authentication
    # DB_AUTH_MODE=windows
    ```
3. **Ensure `.env` is ignored by Git** (Add `.env` to `.gitignore`).  

---

## **3. Verify `.env` File**  
Run this script to check if the values are loaded correctly:

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("\u2705 Database Configuration Loaded:")
print(f"SERVER: {os.getenv('DB_SERVER')}")
print(f"DATABASE: {os.getenv('DB_DATABASE')}")
print(f"AUTH MODE: {os.getenv('DB_AUTH_MODE')}")
print(f"USERNAME: {os.getenv('DB_USERNAME')}")
print(f"PASSWORD: {'*' * len(os.getenv('DB_PASSWORD')) if os.getenv('DB_PASSWORD') else 'Not Set'}")
print(f"DRIVER: {os.getenv('DB_DRIVER')}")
```

---

## **4. Connect to the Database (SQL or Windows Authentication)**  
```python
from pydbmanager.connection import DatabaseConnection

# Initialize and test database connection
db = DatabaseConnection()
conn = db.create_connection()

if conn:
    print("\u2705 Connection Successful!")
    db.close_connection()
else:
    print("\u274c Connection Failed!")
```

---

## **5. Perform SQL Operations**  

### 🔹 **Query Data as DataFrame**  
```python
from pydbmanager.operations import DatabaseOperations

db_ops = DatabaseOperations()
df = db_ops.query_data("SELECT * FROM users", batch_size=5)
print(df)
```

### 🔹 **Insert a New Record**  
```python
insert_query = """
INSERT INTO users (name, email, age, gender, phone_number, address, city, country)
VALUES ('John Doe', 'john.doe@example.com', 29, 'Male', '123-456-7890', '123 Elm St', 'New York', 'USA')
"""
db_ops.execute_query(insert_query)
```

### 🔹 **Update a Record**  
```python
update_query = """
UPDATE users SET age = 30 WHERE email = 'john.doe@example.com'
"""
db_ops.execute_query(update_query)
```

### 🔹 **Delete a Record**  
```python
delete_query = """
DELETE FROM users WHERE email = 'john.doe@example.com'
"""
db_ops.execute_query(delete_query)
```

### 🔹 **Create Table**  
```python
create_table_sql = """
IF NOT EXISTS (
    SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'users'
)
BEGIN
    CREATE TABLE users (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        age INT,
        gender VARCHAR(10),
        phone_number VARCHAR(20),
        address VARCHAR(255),
        city VARCHAR(100),
        country VARCHAR(100)
    );
END
"""
db_ops.create_table(create_table_sql)
```

### 🔹 **Insert a DataFrame to SQL**  
```python
import pandas as pd

# Example DataFrame
df_users = pd.DataFrame([
    {
        'name': 'Jane Smith',
        'email': 'jane.smith@example.com',
        'age': 32,
        'gender': 'Female',
        'phone_number': '555-555-5555',
        'address': '456 Oak Ave',
        'city': 'Chicago',
        'country': 'USA'
    }
])

db_ops.insert_dataframe(df_users, 'users')
```

### 🔹 **Update SQL Table with DataFrame**  

> **Note:** `key_columns` should include the column(s) used to uniquely identify each row (like `id` or `email`). These are used in the SQL `WHERE` clause to apply updates only to matching rows.


```python
# Assume df_users contains updated user data
# Example update: change age for a known email

df_users_update = pd.DataFrame([
    {
        'email': 'jane.smith@example.com',
        'age': 33  # updated age
    }
])

db_ops.update_table_with_dataframe(df_users_update, 'users', key_columns=['email'])

```
---

## **6. Save Query Results to File**  

```python
# Save to CSV
results_df.to_csv("output.csv", index=False)
print("\u2705 Data saved to output.csv")
```

---

## **7. Closing the Connection**  

```python
db_ops.close()
print("\u2705 Database connection closed.")
```

---

## **✅ Congratulations! 🎉**  
You’ve successfully used **PyDBManager** to:
- Connect to SQL Server using SQL or Windows authentication
- Run queries and commands
- Work with DataFrames and tables
- Create, update, and insert into SQL Server tables
- Save data to files and close connections cleanly

---

## **Contributing & License**  
I welcome contributions! Feel free to submit issues and pull requests. 💪  

This project is **MIT Licensed** — you are free to modify and distribute it as needed. 🏆  

🔥 **Happy Coding!** 
