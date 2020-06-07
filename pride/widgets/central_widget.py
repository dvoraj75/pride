from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter
from PyQt5.QtCore import Qt

from pride.common.decorators import file_exception_handling
from pride.widgets import CodeEditorTabWidget
from pride.widgets import OpenedFilesWidget


class CentralIDEWidget(QWidget):
    """
    Central widget of IDE adding together
    main code editor window and file tree/list
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.opened_files_widget = OpenedFilesWidget(self)
        self.code_editor_widget = CodeEditorTabWidget(self)

        self.opened_files_widget.open_file_on_double_click.connect(self.open_file)
        self.code_editor_widget.open_new_file.connect(self.add_file_to_list)
        self.code_editor_widget.change_active_file.connect(self.change_current_active_file)
        self.code_editor_widget.close_file.connect(self.remove_file_from_list)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.opened_files_widget)
        splitter.addWidget(self.code_editor_widget)
        splitter.setSizes([120, 880])

        horizontal_layout = QHBoxLayout()
        horizontal_layout.setSpacing(0)
        horizontal_layout.addWidget(splitter)

        self.setLayout(horizontal_layout)

    @file_exception_handling
    def open_file(self, file_path: str) -> None:
        """
        Just wrapper around CodeEditorTabWidget class

        Args:
            file_path(str): file path
        """
        self.code_editor_widget.open_file(file_path)

    def add_file_to_list(self, file_path: str) -> None:
        """
        Just wrapper around OpenedFilesWidget class

        Args:
            file_path(str): file path
        """
        self.opened_files_widget.add_file(file_path)

    def remove_file_from_list(self, file_path: str) -> None:
        """
        Just wrapper around OpenedFilesWidget class

        Args:
            file_path(str): file path
        """
        self.opened_files_widget.remove_file(file_path)

    def change_current_active_file(self, file_path):
        """
        Just wrapper around OpenedFilesWidget class

        Args:
            file_path(str): file path
        """
        self.opened_files_widget.change_current_active_file(file_path)

    def open_dir(self, dir_path: str) -> None:
        """
        Just wrapper around OpenedFilesWidget class

        Args:
            dir_path(str): file path
        """
        self.opened_files_widget.open_dir(dir_path)
