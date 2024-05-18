# models/user.py
from .database import Database
import hashlib
from mysql.connector import Error

class User:
    def __init__(self, nom, prenom, droit, login, password):
        self.nom = nom
        self.prenom = prenom
        self.droit = droit
        self.login = login
        self.password = self.hash_password(password)

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def save(self):
        connection = Database.connect()
        if connection is None:
            print("Connection to database failed")
            return False

        try:
            cursor = connection.cursor()
            query = "INSERT INTO User (nom, prenom, droit, login, password) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (self.nom, self.prenom, self.droit, self.login, self.password))
            connection.commit()
            return True
        except Error as e:
            print(f"Failed to insert record into User table: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def authenticate(login, password):
        connection = Database.connect()
        if connection is None:
            print("Connection to database failed")
            return False

        try:
            cursor = connection.cursor()
            hashed_password = User.hash_password(password)
            query = "SELECT * FROM User WHERE login = %s AND password = %s"
            cursor.execute(query, (login, hashed_password))
            record = cursor.fetchone()
            return record is not None
        except Error as e:
            print(f"Failed to retrieve record from User table: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

                
    @staticmethod
    def login_exists(login):
        connection = Database.connect()
        if connection is None:
            print("Connection to database failed")
            return False

        try:
            cursor = connection.cursor()
            query = "SELECT * FROM User WHERE login = %s"
            cursor.execute(query, (login,))
            record = cursor.fetchone()
            return record is not None
        except Error as e:
            print(f"Failed to check login in User table: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()