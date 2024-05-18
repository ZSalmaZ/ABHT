# gui/upload_dialog.py
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QFileDialog

class UploadDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Select an Excel file')
        layout = QVBoxLayout()

        label = QLabel('Select an Excel file', self)
        layout.addWidget(label)

        browse_btn = QPushButton('Browse', self)
        browse_btn.clicked.connect(self.load_file)
        layout.addWidget(browse_btn)

        self.setLayout(layout)

    def load_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xls *.xlsx)", options=options)
        if file_path:
            #process_excel(file_path)
            self.accept()
