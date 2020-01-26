
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox

from pride.dialogs.error_dialog import ErrorDialog
from pride.UI.main_window_ui import Ui_MainWindow
from pride.widgets.code_editor import CodeEditorWidget


#  TODO: presunout nekam do konfigurace
#  typy pro file dialogy
ALL_FILES = "All Files (*)"
PYTHON_FILES = "Python files (*.py)"
FILE_TYPES_SEPARATOR = ";;"


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
        self.actionSave_as.triggered.connect(self.save_file_as)

    #  TODO: co nejak modul pro vsechny funkce menu? Je nutne to mit v main window?
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open file", ".", FILE_TYPES_SEPARATOR.join((PYTHON_FILES, ALL_FILES)))

        if not file_path:
            return
        try:
            with open(file_path, 'r') as f:
                self.code_editor.load_file(f)
        except PermissionError:
            #  TODO: logovani
            ErrorDialog("Permission error", "Can't open this file: permission denied", self).show()
        except FileNotFoundError:
            ErrorDialog("File not found", "Can't open this file: file not found", self).show()
        except Exception:
            ErrorDialog("Unknown error", "Can't open this file: unknown error", self).show()

    def save_file_as(self):
        file_path, file_type = QFileDialog.getSaveFileName(self, "Save file as", ".", FILE_TYPES_SEPARATOR.join((PYTHON_FILES, ALL_FILES)))

        if not file_path:
            return

        #  TODO: je to treba? nebude to stacit pridat jenom k vytvareni noveho souboru?
        # if file_type == PYTHON_FILES and not file_path.endswith(".py"):
        #     file_path += ".py"

        try:
            with open(file_path, 'w') as f:
                f.write(self.code_editor.get_plain_text())
        except PermissionError:
            ErrorDialog("Permission error", "Can't save this file: permission denied", self).show()
        except Exception:
            ErrorDialog("Unknown error", "Can't save this file: unknown error", self).show()