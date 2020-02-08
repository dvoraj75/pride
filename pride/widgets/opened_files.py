import os

from PyQt5.QtWidgets import QWidget, QListWidgetItem, QTreeWidgetItem
from PyQt5.QtCore import QSize

from pride.common.decorators import global_instances
from pride.dialogs.error_dialog import ErrorDialog
from pride.UI.item_widget_ui import Ui_ItemWidget
from pride.UI.opened_files_widget_ui import Ui_OpenedFilesWidget


class FileItem(QListWidgetItem):
    def __init__(self, path, parent=None):
        QListWidgetItem.__init__(self, parent)
        self.path = path


class TreeItem(QTreeWidgetItem):
    def __init__(self, tree, strings=None, path=None):
        QTreeWidgetItem.__init__(self, tree, strings)
        self.path = path


class ItemWidget(QWidget, Ui_ItemWidget):
    def __init__(self, file_name, file_path, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.file_name.setText(file_name)
        self.file_path.setText(file_path)


class OpenedFilesWidget(QWidget, Ui_OpenedFilesWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.tree_widget.itemDoubleClicked.connect(self.open_file_on_double_click)
        self.list_widget.itemDoubleClicked.connect(self.open_file_on_double_click)
        self.code_editor = global_instances.get('CentralIDEWidget').code_editor_widget

        self.opened_directories = set()

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
            item = self.list_widget.item(idx)
            if item and item.path == path:
                self.list_widget.takeItem(idx)
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

    def open_dir(self, dir_path: str) -> None:
        """
        Add parent dir to tree and add subdirs.

        Args:
            dir_path(str): base dir path
        """
        if dir_path in self.opened_directories:
            # TODO: set new current dir
            return

        self.opened_directories.add(dir_path)
        parent_folder = TreeItem(self.tree_widget)
        self.tree_widget.setItemWidget(parent_folder, 0, ItemWidget(os.path.basename(dir_path), dir_path))
        self._add_dirs(dir_path, parent_folder)
        print("sorting")

    def _add_dirs(self, path: str, tree: QTreeWidgetItem) -> None:
        """
        Add dirs/files to tree.
        If path is dir call this function recursive.

        Args:
            path(str): base path
            tree(QTreeWidgetItem): tree or subtree
        """
        for element in os.scandir(path):
            parent_item = TreeItem(tree, [os.path.basename(element)], element.path)

            if element.is_dir():
                self._add_dirs(element.path, parent_item)

    def open_file_on_double_click(self, item):
        if item.path and not os.path.isdir(item.path):
            try:
                self.code_editor.open_file(item.path)
            except PermissionError:
                ErrorDialog("Permission error", "Can't open this file: permission denied", self).show()
            except FileNotFoundError:
                ErrorDialog("File not found", "Can't open this file: file not found", self).show()
            except Exception:
                ErrorDialog("Unknown error", "Can't open this file: unknown error", self).show()

