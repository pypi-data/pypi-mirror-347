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
        """
        Execute a SELECT query and return the results as a pandas DataFrame.

        Parameters:
        -----------
        query : str
            A valid SQL SELECT query to execute.

        batch_size : int, optional
            If specified, fetches rows in batches of this size to reduce memory usage.
            If None, fetches all rows at once.

        Returns:
        --------
        pd.DataFrame
            A DataFrame containing the query results, or None if an error occurs.
        """
        self.db.check_connection()
        self.conn = self.db.conn
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
            # print("Data fetched successfully!")
            print("Data Shape", df.shape)
            logging.info(f"Data fetched in {time.time() - start_time:.4f} seconds")
            return df
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()

    def execute_query(self, query: str):
        """
        Execute a non-SELECT SQL query such as INSERT, UPDATE, or DELETE.

        This function automatically retries the query on transient failures using
        the `execute_with_retry` utility wrapper.

        Parameters:
        -----------
        query : str
            The SQL query string to execute. Should not be a SELECT query.

        Returns:
        --------
        bool
            True if the query executed successfully, False otherwise.
        """
        return execute_with_retry(lambda: self._execute_query(query))

    def _execute_query(self, query: str) -> bool:
        """
        Internal method to execute a non-SELECT SQL query directly.

        This function is called by `execute_query()` and is not intended to be used externally.
        It runs the query, commits the transaction, and logs the outcome.

        Parameters:
        -----------
        query : str
            The SQL statement to execute (INSERT, UPDATE, DELETE, or CREATE TABLE).

        Returns:
        --------
        bool
            True if the query executed and committed successfully, False otherwise.
        """
        self.db.check_connection()
        self.conn = self.db.conn

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
        """
        Insert a pandas DataFrame into a specified SQL Server table using SQLAlchemy.

        Parameters:
        -----------
        df : pd.DataFrame
            The DataFrame to be inserted into the SQL table. The column names must match the table schema.

        table_name : str
            The name of the target table in the SQL Server database.

        Returns:
        --------
        bool
            True if the insertion was successful, False otherwise.
        """
        self.db.check_connection()
        self.conn = self.db.conn

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

        """
        Update rows in a SQL Server table using values from a DataFrame.

        Parameters:
        -----------
        df : pd.DataFrame
            The DataFrame containing updated values. Must include both the columns to update
            and the key columns used to match existing records.

        table_name : str
            The name of the SQL Server table to update.

        key_columns : list
            A list of column names that uniquely identify each row in the table (e.g., ['id'] or ['email']).
            These columns will be used in the WHERE clause of the UPDATE statement.

        Returns:
        --------
        bool
            True if all rows were updated successfully, False if an error occurred.
        """
        self.db.check_connection()
        self.conn = self.db.conn

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
        """
        Create a SQL Server table by executing a raw CREATE TABLE SQL statement.

        Parameters:
        -----------
        create_sql : str
            The SQL statement used to create the table. This can include IF NOT EXISTS logic
            to prevent errors if the table already exists.

        Returns:
        --------
        bool
            True if the table creation statement executed successfully, False otherwise.
        """
        return self.execute_query(create_sql)

    def close(self):
        self.db.close_connection()
