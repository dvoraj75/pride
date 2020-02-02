
from PyQt5.QtWidgets import QWidget

from pride.UI.files_tree_widget_ui import Ui_open_files_tree


class FileTreeWidget(QWidget, Ui_open_files_tree):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
