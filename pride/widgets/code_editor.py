import sys

from PyQt5 import QtGui, QtCore, QtWidgets


class CodeEdit(QtWidgets.QPlainTextEdit):
    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == QtCore.Qt.Key_Tab:
            self.textCursor().insertText("    ")
            return
        return QtWidgets.QPlainTextEdit.keyPressEvent(self, e)


class LinesNumberBar(QtWidgets.QWidget):
    def __init__(self, code_editor, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.editor = code_editor

        self.editor.updateRequest.connect(self.update)
        self.editor.blockCountChanged.connect(self.update_width)

        self.update_width('1')

    def update(self) -> None:
        if self.isVisible():
            QtWidgets.QWidget.update(self)

    def update_width(self, line_number: int) -> None:
        """
        Change width for bigger line numbers
        """
        new_width = self.fontMetrics().width(str(line_number)) + 30
        if self.width() != new_width:
            self.setFixedWidth(new_width)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        if self.isVisible():
            block = self.editor.firstVisibleBlock()  # first visible block of editor
            line_number = block.blockNumber()  + 1# line of first visible block
            font_height = self.fontMetrics().height()  # height of used font for line numbers

            painter = QtGui.QPainter(self)  # painter which will draw bar and numbers
            painter.fillRect(event.rect(), QtGui.QColor("#d3d7cf"))  # fill the line number bar with some color TODO: configurable
            painter.drawRect(0, 0, event.rect().width() - 1, event.rect().height() - 1)  # draw line number bar border
            font = painter.font()  # actual font

            current_block = self.editor.textCursor().block().blockNumber() + 1  # line of actual block under cursor

            condition = True
            while block.isValid() and condition:
                block_geometry = self.editor.blockBoundingGeometry(block)
                offset = self.editor.contentOffset()
                block_top = block_geometry.translated(offset).top()

                number_rect = QtCore.QRect(5, block_top, self.width() - 5, font_height)  # rectangle for the line number
                font.setBold(line_number == current_block)  # set bold line number for actual line

                painter.setFont(font)
                painter.drawText(number_rect, QtCore.Qt.AlignLeft, str(line_number))

                line_number += 1

                condition = block_top <= event.rect().bottom()

                block = block.next()

            painter.end()


class CodeEditorWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self._code_editor = CodeEdit(self)
        self._line_number_bar = LinesNumberBar(self._code_editor, self)

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setSpacing(1.5)
        horizontal_layout.addWidget(self._line_number_bar)
        horizontal_layout.addWidget(self._code_editor)

        self.setLayout(horizontal_layout)
