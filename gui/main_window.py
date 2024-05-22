from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QDialog, QLineEdit, QMessageBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from models.user import User

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Data Processing Application')
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # User account icon and label
        self.user_icon_label = QLabel(self)
        self.user_icon_label.setPixmap(QPixmap('gui/images/user.png').scaled(50, 50, Qt.KeepAspectRatio))
        self.user_icon_label.setAlignment(Qt.AlignCenter)
        self.user_icon_label.mousePressEvent = self.show_account_info  # Making the label clickable

        self.user_text_label = QLabel('My Account', self)
        self.user_text_label.setAlignment(Qt.AlignCenter)
        self.user_text_label.mousePressEvent = self.show_account_info  # Making the label clickable

        user_layout = QVBoxLayout()
        user_layout.addWidget(self.user_icon_label)
        user_layout.addWidget(self.user_text_label)

        user_widget = QWidget()
        user_widget.setLayout(user_layout)

        layout.addWidget(user_widget, alignment=Qt.AlignLeft | Qt.AlignBottom)

        if self.user["droit"] == 'admin':
            self.visualise_users_btn = QPushButton('Visualise All Users', self)
            self.visualise_users_btn.clicked.connect(self.visualise_all_users)
            layout.addWidget(self.visualise_users_btn)

        central_widget.setLayout(layout)
        self.setGeometry(300, 300, 400, 300)
        self.show()

    def show_account_info(self, event):
        dialog = AccountInfoDialog(self.user)
        dialog.exec_()

    def visualise_all_users(self):
        dialog = VisualiseUsersDialog()
        dialog.exec_()

class AccountInfoDialog(QDialog):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My Account')
        layout = QVBoxLayout()

        self.name_label = QLabel(f'Name: {self.user["prenom"]}', self)
        layout.addWidget(self.name_label)

        self.last_name_label = QLabel(f'Last Name: {self.user["nom"]}', self)
        layout.addWidget(self.last_name_label)

        self.login_label = QLabel(f'Login: {self.user["login"]}', self)
        layout.addWidget(self.login_label)

        self.change_password_btn = QPushButton('Change Password', self)
        self.change_password_btn.clicked.connect(self.open_change_password_dialog)
        layout.addWidget(self.change_password_btn)

        self.setLayout(layout)

    def open_change_password_dialog(self):
        dialog = ChangePasswordDialog(self.user)
        dialog.exec_()

class ChangePasswordDialog(QDialog):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Change Password')
        layout = QVBoxLayout()

        self.old_password_label = QLabel('Old Password:')
        self.old_password_input = QLineEdit(self)
        self.old_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.old_password_label)
        layout.addWidget(self.old_password_input)

        self.new_password_label = QLabel('New Password:')
        self.new_password_input = QLineEdit(self)
        self.new_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.new_password_label)
        layout.addWidget(self.new_password_input)

        self.confirm_password_label = QLabel('Confirm New Password:')
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_input)

        self.change_password_btn = QPushButton('Change Password', self)
        self.change_password_btn.clicked.connect(self.change_password)
        layout.addWidget(self.change_password_btn)

        self.setLayout(layout)

    def change_password(self):
        old_password = self.old_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if new_password != confirm_password:
            QMessageBox.warning(self, 'Error', 'New passwords do not match')
            return

        if User.change_password(self.user["login"], old_password, new_password):
            QMessageBox.information(self, 'Success', 'Password changed successfully')
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Failed to change password')

class VisualiseUsersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('All Users')
        layout = QVBoxLayout()

        self.users_table = QTableWidget()
        self.users_table.setColumnCount(5)
        self.users_table.setHorizontalHeaderLabels(['Prenom', 'Nom', 'Login', 'Droit', 'Delete'])
        self.users_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.users_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.users = User.get_all_users()
        self.users_table.setRowCount(len(self.users))

        for row, user in enumerate(self.users):
            self.users_table.setItem(row, 0, QTableWidgetItem(user['prenom']))
            self.users_table.setItem(row, 1, QTableWidgetItem(user['nom']))
            self.users_table.setItem(row, 2, QTableWidgetItem(user['login']))
            self.users_table.setItem(row, 3, QTableWidgetItem(user['droit']))
            delete_button = QPushButton('Delete')
            delete_button.clicked.connect(lambda _, u=user: self.delete_user(u))
            self.users_table.setCellWidget(row, 4, delete_button)

        layout.addWidget(self.users_table)
        self.setLayout(layout)

    def delete_user(self, user):
        if User.delete_user(user["login"]):
            QMessageBox.information(self, 'Success', f'User {user["login"]} deleted successfully')
            self.refresh_users_table()
        else:
            QMessageBox.warning(self, 'Error', f'Failed to delete user {user["login"]}')

    def refresh_users_table(self):
        self.users = User.get_all_users()
        self.users_table.setRowCount(len(self.users))
        for row, user in enumerate(self.users):
            self.users_table.setItem(row, 0, QTableWidgetItem(user['prenom']))
            self.users_table.setItem(row, 1, QTableWidgetItem(user['nom']))
            self.users_table.setItem(row, 2, QTableWidgetItem(user['login']))
            self.users_table.setItem(row, 3, QTableWidgetItem(user['droit']))
            delete_button = QPushButton('Delete')
            delete_button.clicked.connect(lambda _, u=user: self.delete_user(u))
            self.users_table.setCellWidget(row, 4, delete_button)
