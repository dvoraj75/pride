from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter
from PyQt5.QtCore import Qt

from pride.widgets import CodeEditorTabWidget
from pride.widgets import FileTreeWidget


class CentralIDEWidget(QWidget):
    """
    Central widget of IDE adding together
    main code editor window and file tree/list
    """

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
