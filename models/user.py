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
            cursor = connection.cursor(dictionary=True)
            hashed_password = User.hash_password(password)
            query = "SELECT * FROM User WHERE login = %s AND password = %s"
            cursor.execute(query, (login, hashed_password))
            record = cursor.fetchone()
            return record
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

    @staticmethod
    def change_password(login, old_password, new_password):
        connection = Database.connect()
        if connection is None:
            print("Connection to database failed")
            return False

        try:
            cursor = connection.cursor()
            hashed_old_password = User.hash_password(old_password)
            query = "SELECT * FROM User WHERE login = %s AND password = %s"
            cursor.execute(query, (login, hashed_old_password))
            record = cursor.fetchone()
            if record:
                hashed_new_password = User.hash_password(new_password)
                update_query = "UPDATE User SET password = %s WHERE login = %s"
                cursor.execute(update_query, (hashed_new_password, login))
                connection.commit()
                return True
            else:
                return False
        except Error as e:
            print(f"Failed to update password: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_all_users():
        connection = Database.connect()
        if connection is None:
            print("Connection to database failed")
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM User"
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except Error as e:
            print(f"Failed to retrieve users: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def delete_user(login):
        connection = Database.connect()
        if connection is None:
            print("Connection to database failed")
            return False

        try:
            cursor = connection.cursor()
            query = "DELETE FROM User WHERE login = %s"
            cursor.execute(query, (login,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Failed to delete user: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
