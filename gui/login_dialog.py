# gui/login_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from models.user import User

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')
        layout = QVBoxLayout()

        self.login_label = QLabel('Login:')
        self.login_input = QLineEdit(self)
        layout.addWidget(self.login_label)
        layout.addWidget(self.login_input)

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_btn = QPushButton('Login', self)
        self.login_btn.clicked.connect(self.authenticate)
        layout.addWidget(self.login_btn)

        self.register_btn = QPushButton('Register', self)
        self.register_btn.clicked.connect(self.open_register_dialog)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

    def authenticate(self):
        login = self.login_input.text()
        password = self.password_input.text()
        if User.authenticate(login, password):
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Incorrect login or password')

    def open_register_dialog(self):
        from .register_dialog import RegisterDialog
        dialog = RegisterDialog(self)
        dialog.exec_()
