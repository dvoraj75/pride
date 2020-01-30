
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from pride.dialogs.error_dialog import ErrorDialog
from pride.dialogs.question_dialog import QuestionDialog
from pride.UI.main_window_ui import Ui_MainWindow
from pride.widgets.code_editor import CodeEditorTabWidget


#  TODO: presunout nekam do konfigurace
#  typy pro file dialogy
ALL_FILES = "All Files (*)"
PYTHON_FILES = "Python files (*.py)"
FILE_TYPES_SEPARATOR = ";;"


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.code_editor = CodeEditorTabWidget(self)
        self.horizontal_layout.addWidget(self.code_editor)
        self.vertical_layout.addLayout(self.horizontal_layout)
        self.centralwidget.setLayout(self.vertical_layout)

        self.trigger_menu_actions()

    def trigger_menu_actions(self):
        # self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        # self.actionSave.triggered.connect(self.save_file)
        # self.actionSave_as.triggered.connect(self.save_file_as)
        # self.actionExit.triggered.connect(self.exit_application)

    # #  TODO: co nejak modul pro vsechny funkce menu? Je nutne to mit v main window?
    # #  TODO: kvuli tomu, ze zde volam save_file_as se ve file dialogu zobrazuje Save file - upravit
    # def new_file(self):
    #     file_path, _ = QFileDialog.getSaveFileName(self, "New file", ".", FILE_TYPES_SEPARATOR.join((PYTHON_FILES, ALL_FILES)))
    #
    #     if not file_path:
    #         return
    #
    #     try:
    #         with open(file_path, 'w') as f:
    #             f.write("")
    #     except PermissionError:
    #         ErrorDialog("Permission error", "Can't create this file: permission denied", self).show()
    #     except Exception:
    #         ErrorDialog("Unknown error", "Can't create this file: unknown error", self).show()
    #
    #     self.code_editor.opened_file = file_path
    # #
    def open_file(self):
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
        except Exception as e:
            ErrorDialog("Unknown error", "Can't open this file: unknown error", self).show()
            print(e)
    #
    # def save_file(self):
    #     file_path = self.code_editor.opened_file
    #
    #     if not file_path:
    #         return self.save_file_as()
    #
    #     try:
    #         with open(file_path, 'w') as f:
    #             f.write(self.code_editor.get_plain_text())
    #     except PermissionError:
    #         ErrorDialog("Permission error", "Can't save this file: permission denied", self).show()
    #     except Exception:
    #         ErrorDialog("Unknown error", "Can't save this file: unknown error", self).show()
    #
    # def save_file_as(self):
    #     file_path, _ = QFileDialog.getSaveFileName(self, "Save file", ".", FILE_TYPES_SEPARATOR.join((PYTHON_FILES, ALL_FILES)))
    #
    #     if not file_path:
    #         return
    #
    #     try:
    #         with open(file_path, 'w') as f:
    #             f.write(self.code_editor.get_plain_text())
    #     except PermissionError:
    #         ErrorDialog("Permission error", "Can't save this file: permission denied", self).show()
    #     except Exception:
    #         ErrorDialog("Unknown error", "Can't save this file: unknown error", self).show()
    #
    #     self.code_editor.opened_file = file_path
    #
    # def exit_application(self):
    #     #  TODO: soubor neni ulozen !!
    #     self.close()
