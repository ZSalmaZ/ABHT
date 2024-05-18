# gui/main_window.py
from PyQt5.QtWidgets import QMainWindow, QPushButton, QFileDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Data Processing Application')

        upload_btn = QPushButton('Upload Excel', self)
        upload_btn.clicked.connect(self.open_upload_dialog)
        upload_btn.resize(upload_btn.sizeHint())
        upload_btn.move(50, 50)

        self.setGeometry(300, 300, 400, 300)
        self.show()

    def open_upload_dialog(self):
        from .upload_dialog import UploadDialog
        dialog = UploadDialog(self)
        dialog.exec_()
