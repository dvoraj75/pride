from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter
from PyQt5.QtCore import Qt

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

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.opened_files_widget)
        splitter.addWidget(self.code_editor_widget)
        splitter.setSizes([120, 880])

        horizontal_layout = QHBoxLayout()
        horizontal_layout.setSpacing(0)
        horizontal_layout.addWidget(splitter)

        self.setLayout(horizontal_layout)

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
