import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class Database:
    @staticmethod
    def connect():
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None