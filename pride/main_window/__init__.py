
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from pride.generated.main_window_ui import Ui_MainWindow
from pride.main_window.widgets.code_editor import CodeEditorWidget


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        code_editor = CodeEditorWidget()
        self.horizontal_layout.addWidget(code_editor)
        self.centralwidget.setLayout(self.horizontal_layout)
