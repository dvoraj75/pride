import os

from PyQt5.QtWidgets import QWidget, QListWidgetItem
from PyQt5.QtCore import QSize

from pride.UI.opened_files_widget_ui import Ui_OpenedFilesWidget
from pride.UI.list_item_widget_ui import Ui_ListItemWidget


class FileItem(QListWidgetItem):
    def __init__(self, path, parent=None):
        QListWidgetItem.__init__(self, parent)
        self.path = path


class ItemWidget(QWidget, Ui_ListItemWidget):
    def __init__(self, file_name, file_path, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.file_name.setText(file_name)
        self.file_path.setText(file_path)


class OpenedFilesWidget(QWidget, Ui_OpenedFilesWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

    def add_file(self, path: str) -> None:
        """
        Add new file to the list widget

        Args:
            path(str): file path
        """
        item = FileItem(path)
        item.setSizeHint(QSize(0, 25))
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, ItemWidget(os.path.basename(path), path))
        self.change_current_row(self.list_widget.count() - 1)

    def remove_file(self, path: str) -> None:
        """
        Remove file from list widget

        Args:
            path(str): file path
        """
        for idx in range(self.list_widget.count()):
            item = self.list_widget.takeItem(idx)
            if item and item.path == path:
                self.list_widget.removeItemWidget(item)
                break

    def change_current_active_file(self, file_path):
        """
        Find index of file and set it as active

        Args:
            file_path(str): file path
        """
        for idx in range(self.list_widget.count()):
            item = self.list_widget.item(idx)
            if item and item.path == file_path:
                self.change_current_row(idx)
                break

    def change_current_row(self, idx: int) -> None:
        """
        Change current active row.

        Args:
            idx(int): index of row
        """
        self.list_widget.setCurrentRow(idx)
