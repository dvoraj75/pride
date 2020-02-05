
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QToolBar, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor

from pride.dialogs.error_dialog import ErrorDialog
from pride.UI.main_window_ui import Ui_MainWindow
from pride.widgets import CentralIDEWidget


#  TODO: presunout nekam do konfigurace
#  typy pro file dialogy
ALL_FILES = "All Files (*)"
PYTHON_FILES = "Python files (*.py)"
FILE_TYPES_SEPARATOR = ";;"


class StatusBarWidget(QWidget):
    """
    Simple status bar widget for main information
    like line and column of cursor, git branch, python version.
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        horizontal_layout = QHBoxLayout(self)

        horizontal_spacer = QSpacerItem(400, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        horizontal_layout.addItem(horizontal_spacer)

        self.line_and_column_label = QLabel(self)
        self.line_and_column_pattern = "line:{} column:{}"

        horizontal_layout.addWidget(self.line_and_column_label)

    def set_line_and_column(self, line: int, column: int) -> None:
        """
        Set new values to line and column label

        Args:
            line(int): line number
            column(int): column number
        """
        self.line_and_column_label.setText(self.line_and_column_pattern.format(line, column))


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main window class representing the main window of app.
    """
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.central_ide_widget = CentralIDEWidget(self)
        self.code_editor = self.central_ide_widget.code_editor_widget
        self.horizontal_layout.addWidget(self.central_ide_widget)
        self.vertical_layout.addLayout(self.horizontal_layout)

        self.bottom_tool_bar = QToolBar(self)
        self.bottom_tool_bar.setMovable(False)
        self.bottom_tool_bar.setAllowedAreas(Qt.BottomToolBarArea)
        self.addToolBar(Qt.BottomToolBarArea, self.bottom_tool_bar)
        self.bottom_tool_bar.addAction("bottom tool bar")

        self.statusbar_widget = StatusBarWidget(self.statusbar)
        self.statusbar.addPermanentWidget(self.statusbar_widget, 1)

        self.trigger_menu_actions()

    def trigger_menu_actions(self) -> None:
        """
        Trigger all actions in menu
        """
        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionOpen_folder.triggered.connect(self.open_dir)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSave_as.triggered.connect(self.save_file_as)
        self.actionExit.triggered.connect(self.exit_application)

    def set_new_cursor_position(self, cursor: QTextCursor) -> None:
        """
        Set new cursor position in main status bar

        Args:
            cursor(QTextCursor): active cursor of code editor in active tab
        """
        self.statusbar_widget.set_line_and_column(
            cursor.block().blockNumber() + 1,
            cursor.positionInBlock() + 1
        )

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
            ErrorDialog("Permission error", "Can't open this file: permission denied", self).show()
        except FileNotFoundError:
            ErrorDialog("File not found", "Can't open this file: file not found", self).show()
        except Exception:
            ErrorDialog("Unknown error", "Can't open this file: unknown error", self).show()

    def open_dir(self) -> None:
        """
        Open directory
        """
        dir_path = QFileDialog.getExistingDirectory(self, "Open folder", "./", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

        if not dir_path:
            return

        try:
            self.central_ide_widget.open_dir(dir_path)
        except PermissionError:
            ErrorDialog("Permission error", "Can't open this directory: permission denied", self).show()
        except FileNotFoundError:
            ErrorDialog("File not found", "Can't open this directory: directory not found", self).show()
        except Exception:
            ErrorDialog("Unknown error", "Can't open this directory: unknown error", self).show()

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
