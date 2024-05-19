# main.py
import sys
from PyQt5.QtWidgets import QApplication, QDialog
from gui.main_window import MainWindow
from gui.login_dialog import LoginDialog
from models.user import User

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        user = User.authenticate(login_dialog.login_input.text(), login_dialog.password_input.text())
        if user:
            main_window = MainWindow(user)
            main_window.show()
            sys.exit(app.exec_())
    else:
        sys.exit(0)
