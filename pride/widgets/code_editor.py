
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QKeyEvent, QPaintEvent, QPainter, QColor
from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QHBoxLayout


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

        self.__opened_file = None

    @property
    def opened_file(self):
        return self.__opened_file

    @opened_file.setter
    def opened_file(self, file_name):
        self.__opened_file = file_name

    def load_file(self, file):
        self._code_editor.clear()
        for line in file:
            self._code_editor.insertPlainText(line)

        self.__opened_file = file.name

    def get_plain_text(self):
        return self._code_editor.toPlainText()

