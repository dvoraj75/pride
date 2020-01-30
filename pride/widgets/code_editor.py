import os

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QKeyEvent, QPaintEvent, QPainter, QColor, QMouseEvent
from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QTabBar


class CodeEdit(QPlainTextEdit):
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Tab:
            self.textCursor().insertText("    ")
            return
        return QPlainTextEdit.keyPressEvent(self, event)


class LinesNumberBar(QWidget):
    def __init__(self, code_editor, parent=None):
        QWidget.__init__(self, parent)
        self.editor = code_editor

        self.editor.updateRequest.connect(self.update)
        self.editor.blockCountChanged.connect(self.update_width)

        self.update_width('1')

    def update(self) -> None:
        if self.isVisible():
            QWidget.update(self)

    def update_width(self, line_number: int) -> None:
        """
        Change width for bigger line numbers
        """
        new_width = self.fontMetrics().width(str(line_number)) + 30
        if self.width() != new_width:
            self.setFixedWidth(new_width)

    def paintEvent(self, event: QPaintEvent) -> None:
        if self.isVisible():
            block = self.editor.firstVisibleBlock()  # first visible block of editor
            line_number = block.blockNumber()  + 1# line of first visible block
            font_height = self.fontMetrics().height()  # height of used font for line numbers

            painter = QPainter(self)  # painter which will draw bar and numbers
            painter.fillRect(event.rect(), QColor("#d3d7cf"))  # fill the line number bar with some color TODO: configurable
            painter.drawRect(0, 0, event.rect().width() - 1, event.rect().height() - 1)  # draw line number bar border
            font = painter.font()  # actual font

            current_block = self.editor.textCursor().block().blockNumber() + 1  # line of actual block under cursor

            condition = True
            while block.isValid() and condition:
                block_geometry = self.editor.blockBoundingGeometry(block)
                offset = self.editor.contentOffset()
                block_top = block_geometry.translated(offset).top()

                number_rect = QRect(5, block_top, self.width() - 5, font_height)  # rectangle for the line number
                font.setBold(line_number == current_block)  # set bold line number for actual line

                painter.setFont(font)
                painter.drawText(number_rect, Qt.AlignLeft, str(line_number))

                line_number += 1

                condition = block_top <= event.rect().bottom()

                block = block.next()

            painter.end()


class CodeEditorWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self._code_editor = CodeEdit(self)
        self._line_number_bar = LinesNumberBar(self._code_editor, self)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.setSpacing(1.5)
        horizontal_layout.addWidget(self._line_number_bar)
        horizontal_layout.addWidget(self._code_editor)

        self.setLayout(horizontal_layout)

        self.file_saved = True

    def load_file(self, file):
        self._code_editor.clear()
        for line in file:
            self._code_editor.insertPlainText(line)

    def get_plain_text(self):
        return self._code_editor.toPlainText()

    def is_modified(self):
        return self._code_editor.document().isModified()


class TabBar(QTabBar):
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MidButton:
            self.tabCloseRequested.emit(self.tabAt(event.pos()))


class CodeEditorTabWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        vertical_layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabBar(TabBar())
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setUsesScrollButtons(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        vertical_layout.addWidget(self.tab_widget)
        self.setLayout(vertical_layout)

    def open_file(self, file_path: str):
        with open(file_path, 'r') as f:
            code_editor = CodeEditorWidget(self)
            code_editor.load_file(f)
            code_editor.file_saved = True
            self.add_tab(code_editor, f.name)

    def add_tab(self, code_editor: CodeEditorWidget, file_name: str):
        new_index = self.tab_widget.count()
        self.tab_widget.addTab(code_editor, os.path.basename(file_name))
        self.tab_widget.setCurrentIndex(new_index)

    def close_tab(self, index):
        self.tab_widget.removeTab(index)
