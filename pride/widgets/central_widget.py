from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter
from PyQt5.QtCore import Qt

from pride.widgets.code_editor import CodeEditorTabWidget
from pride.widgets.file_tree import FileTreeWidget


class CentralIDEWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.file_tree_widget = FileTreeWidget(self)
        self.code_editor_widget = CodeEditorTabWidget(self)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.file_tree_widget)
        splitter.addWidget(self.code_editor_widget)
        splitter.setSizes([120, 880])

        horizontal_layout = QHBoxLayout()
        horizontal_layout.setSpacing(0)
        horizontal_layout.addWidget(splitter)

        self.setLayout(horizontal_layout)
