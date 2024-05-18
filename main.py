# main.py
import sys
from PyQt5.QtWidgets import QApplication, QDialog
from gui.main_window import MainWindow
from gui.login_dialog import LoginDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)
