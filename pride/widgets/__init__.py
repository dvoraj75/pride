
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from pride.UI.main_window_ui import Ui_MainWindow
from pride.widgets.code_editor import CodeEditorWidget


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.code_editor = CodeEditorWidget(self)
        self.horizontal_layout.addWidget(self.code_editor)
        self.vertical_layout.addLayout(self.horizontal_layout)
        self.centralwidget.setLayout(self.vertical_layout)

        self.trigger_menu_actions()

    def trigger_menu_actions(self):
        self.actionOpen.triggered.connect(self.open_file)

    #  TODO: co nejak modul pro vsechny funkce menu? Je nutne to mit v main window?
    #  TODO: exceptions
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open file", ".", "Python files (*.py);; all Files (*)")

        if not file_path:
            return

        with open(file_path, 'r') as f:
            self.code_editor.load_file(f)
