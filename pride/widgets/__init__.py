
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from pride.dialogs.error_dialog import ErrorDialog
from pride.UI.main_window_ui import Ui_MainWindow
from pride.widgets.code_editor import CodeEditorTabWidget


#  TODO: presunout nekam do konfigurace
#  typy pro file dialogy
ALL_FILES = "All Files (*)"
PYTHON_FILES = "Python files (*.py)"
FILE_TYPES_SEPARATOR = ";;"


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main window class representing the main window of app.
    """
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.code_editor = CodeEditorTabWidget(self)
        self.horizontal_layout.addWidget(self.code_editor)
        self.vertical_layout.addLayout(self.horizontal_layout)
        self.centralwidget.setLayout(self.vertical_layout)

        self.trigger_menu_actions()

    def trigger_menu_actions(self) -> None:
        """
        Trigger all actions in menu
        """
        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSave_as.triggered.connect(self.save_file_as)
        self.actionExit.triggered.connect(self.exit_application)

    def new_file(self) -> None:
        """
        Create new tab / file
        """
        self.code_editor.new_file()

    def open_file(self) -> None:
        """
        Open file in new tab.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Open file", ".", FILE_TYPES_SEPARATOR.join((PYTHON_FILES, ALL_FILES)))

        if not file_path:
            return
        try:
            self.code_editor.open_file(file_path)
        except PermissionError:
            #  TODO: logovani
            ErrorDialog("Permission error", "Can't open this file: permission denied", self).show()
        except FileNotFoundError:
            ErrorDialog("File not found", "Can't open this file: file not found", self).show()
        except Exception:
            ErrorDialog("Unknown error", "Can't open this file: unknown error", self).show()

    def save_file(self) -> None:
        """
        Save file in active tab.
        """
        if not self.code_editor.opened_tabs:
            return

        if not self.code_editor.is_file_saved():
            return self.save_file_as()

        try:
            self.code_editor.save_file()
        except PermissionError:
            ErrorDialog("Permission error", "Can't save this file: permission denied", self).show()
        except Exception as e:
            ErrorDialog("Unknown error", "Can't save this file: unknown error", self).show()

    def save_file_as(self) -> None:
        """
        Save as file in active tab
        """
        if not self.code_editor.opened_tabs:
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save file", ".", FILE_TYPES_SEPARATOR.join((PYTHON_FILES, ALL_FILES)))

        if not file_path:
            return

        try:
            self.code_editor.save_file(file_path)
        except PermissionError:
            ErrorDialog("Permission error", "Can't save this file: permission denied", self).show()
        except Exception:
            ErrorDialog("Unknown error", "Can't save this file: unknown error", self).show()

    def exit_application(self) -> None:
        """
        Close app
        """
        self.close()
