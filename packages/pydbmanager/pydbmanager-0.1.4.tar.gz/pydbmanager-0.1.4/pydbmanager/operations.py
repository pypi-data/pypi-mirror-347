import pandas as pd
import time
import logging
from sqlalchemy import create_engine
import urllib
from pydbmanager.connection import DatabaseConnection
from pydbmanager.utils import execute_with_retry

class DatabaseOperations:
    """Handles database queries and operations."""

    def __init__(self):
        self.db = DatabaseConnection()
        self.conn = self.db.create_connection()
        self.connection_string = self.db.get_connection_string()

    def query_data(self, query: str, batch_size: int = None):
        self.db.check_connection()
        if self.conn is None:
            logging.error("No active database connection.")
            return None

        start_time = time.time()
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            rows = []
            if batch_size:
                while True:
                    batch = cursor.fetchmany(batch_size)
                    if not batch:
                        break
                    rows.extend(batch)
            else:
                rows = cursor.fetchall()

            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame.from_records(rows, columns=columns)
            print("Data fetched successfully!")
            print("Dataframe Size", df.shape)
            logging.info(f"Data fetched in {time.time() - start_time:.4f} seconds")
            return df
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()

    def execute_query(self, query: str):
        return execute_with_retry(lambda: self._execute_query(query))

    def _execute_query(self, query: str) -> bool:
        self.db.check_connection()
        if self.conn is None:
            logging.error("No active database connection.")
            return False

        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            logging.info("Query executed successfully!")
            return True
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()

    def insert_dataframe(self, df: pd.DataFrame, table_name: str):
        """Insert DataFrame into SQL Server using SQLAlchemy."""
        self.db.check_connection()
        if self.conn is None:
            logging.error("No active database connection.")
            return False

        try:
            engine = create_engine(f"mssql+pyodbc:///?odbc_connect={self.connection_string}")
            df.to_sql(table_name, engine, if_exists='append', index=False)
            logging.info(f"Inserted DataFrame into table '{table_name}' successfully!")
            return True
        except Exception as e:
            logging.error(f"Error inserting DataFrame: {e}")
            return False

    def update_table_with_dataframe(self, df: pd.DataFrame, table_name: str, key_columns: list):
        self.db.check_connection()
        if self.conn is None:
            logging.error("No active database connection.")
            return False

        try:
            cursor = self.conn.cursor()
            for _, row in df.iterrows():
                set_clause = ", ".join([f"{col} = ?" for col in df.columns if col not in key_columns])
                where_clause = " AND ".join([f"{key} = ?" for key in key_columns])
                values = [row[col] for col in df.columns if col not in key_columns] + [row[key] for key in key_columns]
                sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
                cursor.execute(sql, values)

            self.conn.commit()
            logging.info(f"Updated table '{table_name}' successfully using DataFrame.")
            return True
        except Exception as e:
            logging.error(f"Error updating table with DataFrame: {e}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()

    def create_table(self, create_sql: str):
        return self.execute_query(create_sql)

    def close(self):
        self.db.close_connection()
