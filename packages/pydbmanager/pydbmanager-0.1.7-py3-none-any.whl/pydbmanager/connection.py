import pyodbc
import logging
import urllib
from pydbmanager.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DatabaseConnection:
    """Handles database connection management."""

    def __init__(self):
        self.conn = None

    def create_connection(self):
        if Config.AUTH_MODE.lower() == "windows":
            connection_string = (
                f"DRIVER={Config.DRIVER};"
                f"SERVER={Config.SERVER};"
                f"DATABASE={Config.DATABASE};"
                "Trusted_Connection=yes;"
                "TrustServerCertificate=yes;"
            )
        else:  # SQL Server Authentication
            connection_string = (
                f"DRIVER={Config.DRIVER};"
                f"SERVER={Config.SERVER};"
                f"DATABASE={Config.DATABASE};"
                f"UID={Config.USERNAME};"
                f"PWD={Config.PASSWORD};"
                "TrustServerCertificate=yes;"
            )

        try:
            self.conn = pyodbc.connect(connection_string)
            logging.info("Database connection established successfully.")
            return self.conn
        except pyodbc.Error as e:
            logging.error(f"Database connection failed: {e}")
            return None


    def get_connection_string(self):

        if Config.AUTH_MODE.lower() == "windows":
            conn_str = (
                f"DRIVER={Config.DRIVER};"
                f"SERVER={Config.SERVER};"
                f"DATABASE={Config.DATABASE};"
                "Trusted_Connection=yes;"
                "TrustServerCertificate=yes;"
            )
        else:
            conn_str = (
                f"DRIVER={Config.DRIVER};"
                f"SERVER={Config.SERVER};"
                f"DATABASE={Config.DATABASE};"
                f"UID={Config.USERNAME};"
                f"PWD={Config.PASSWORD};"
                "TrustServerCertificate=yes;"
            )

        return urllib.parse.quote_plus(conn_str)


    def check_connection(self):
        """Ensures the database connection is active, reconnecting if necessary"""
        if self.conn is None:
            logging.warning("No active connection. Attempting to reconnect...")
            self.conn = self.create_connection()

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT 1")
        except (pyodbc.Error, AttributeError):
            logging.warning("Database connection lost. Reconnecting...")
            self.conn = self.create_connection()

    def close_connection(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            logging.info("Database connection closed")
