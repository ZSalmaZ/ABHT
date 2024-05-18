# gui/register_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from models.user import User

class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Register')
        layout = QVBoxLayout()

        self.nom_label = QLabel('Nom:')
        self.nom_input = QLineEdit(self)
        layout.addWidget(self.nom_label)
        layout.addWidget(self.nom_input)

        self.prenom_label = QLabel('Prenom:')
        self.prenom_input = QLineEdit(self)
        layout.addWidget(self.prenom_label)
        layout.addWidget(self.prenom_input)

        self.login_label = QLabel('Login:')
        self.login_input = QLineEdit(self)
        layout.addWidget(self.login_label)
        layout.addWidget(self.login_input)

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.register_btn = QPushButton('Register', self)
        self.register_btn.clicked.connect(self.register)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

    def register(self):
        nom = self.nom_input.text()
        prenom = self.prenom_input.text()
        login = self.login_input.text()
        password = self.password_input.text()
        droit = 'user'  

        if not all([nom, prenom, login, password]):
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')
        elif User.login_exists(login):
            QMessageBox.warning(self, 'Error', 'Login already exists')
        else:
            user = User(nom, prenom, droit, login, password)
            if user.save():
                QMessageBox.information(self, 'Success', 'User registered successfully')
                self.accept()
            else:
                QMessageBox.warning(self, 'Error', 'Failed to register user')
