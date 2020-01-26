
from PyQt5.QtWidgets import QMessageBox


class ErrorDialog(QMessageBox):
    def __init__(self, dialog_title, error_message, parent=None):
        QMessageBox.__init__(self, parent)
        self.setIcon(self.Critical)
        self.setText(error_message)
        self.setWindowTitle(dialog_title)
