import os
import typing

from PyQt5.QtCore import Qt, QRect, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QPaintEvent, QPainter, QColor, QMouseEvent, QTextCursor, QWheelEvent
from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QTabBar, QStatusBar


class CodeEdit(QPlainTextEdit):
    """
    Simple inherited class from QPlainTextEdit
    for overriding keyPressEvent.
    """
    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Overridden keyPressEvent which adjust default behaviour of
        key tab.

        Args:
            event(QKeyEvent): qt event object with event data
        """
        if event.key() == Qt.Key_Tab:
            self.textCursor().insertText("    ")
            return
        return QPlainTextEdit.keyPressEvent(self, event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        """
        Overridden wheelEvent for zooming.
        Args:
            event(QWheelEvent): qt event object with event data
        """
        if event.modifiers() & Qt.ControlModifier:
            self.zoom(event.angleDelta().y())
        else:
            QPlainTextEdit.wheelEvent(self, event)

    def zoom(self, delta: int) -> None:
        """
        Zoom text in editor
        Args:
            delta(int): delta which represent zoomin or zoomout

        """
        if delta > 0:
            self.zoomIn(1)
        elif delta < 0:
            self.zoomOut(1)


class LinesNumberBar(QWidget):
    """
    This object is representing object wit lines number.
    LinesNumber bar is connected with CodeEdit.
    It cant work separately.
    """
    def __init__(self, code_editor: CodeEdit, parent=None):
        QWidget.__init__(self, parent)
        self.editor = code_editor

        self.editor.updateRequest.connect(self.update)
        self.editor.blockCountChanged.connect(self.update_width)

        self.update_width(1)

    def update(self) -> None:
        """
        Overridden update method of QWidget.
        Schedule a paint event for processing only
        if widget is visible.
        """
        if self.isVisible():
            QWidget.update(self)

    def update_width(self, line_number: int) -> None:
        """
        Change lines bar width. Depends on line number width.

        Args:
            line_number(int): line number
        """
        new_width = self.fontMetrics().width(str(line_number)) + 30
        if self.width() != new_width:
            self.setFixedWidth(new_width)

    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Overridden paintEvent of QWidget which repainting numbers in bar.

        Args:
            event(QPaintEvent): qt event object with event data
        """
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
    """
    Widget which representing code editor with lines number bar.
    """

    change_cursor_position = pyqtSignal(int, int)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self._code_editor = CodeEdit(self)
        self._code_editor.cursorPositionChanged.connect(self.cursor_position_changed)
        self._line_number_bar = LinesNumberBar(self._code_editor, self)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.setSpacing(0)
        horizontal_layout.addWidget(self._line_number_bar)
        horizontal_layout.addWidget(self._code_editor)

        self.setLayout(horizontal_layout)

        self.file_saved = True
        self.opened_file = None

    def cursor_position_changed(self):
        """
        This method is called when cursorPositionChanged signal is emitted.
        """
        self.change_cursor_position.emit(
            self.get_cursor().block().blockNumber() + 1,
            self.get_cursor().positionInBlock() + 1
        )

    def load_file(self, file: typing.TextIO) -> None:
        """
        Load text from file to code editor.

        Args:
            file(typing.TextIO): opened file in code editor
        """
        self._code_editor.clear()
        for line in file:
            self._code_editor.insertPlainText(line)

    def get_plain_text(self) -> str:
        """
        Return text from code editor.

        Returns:
            str: text from code_editor
        """
        return self._code_editor.toPlainText()

    def get_cursor(self) -> QTextCursor:
        """
        Returns active cursor of text widget

        Returns:
            QTextCursor: active cursor
        """
        return self._code_editor.textCursor()


class TabBar(QTabBar):
    """
    Simple inherited class from QTabBar
    for Overriding mouseReleaseEvent.
    """
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        Overridden method for closing tab with middle mouse button.

        Args:
            event(QMouseEvent): qt event object with event data:
        """
        if event.button() == Qt.MidButton:
            self.tabCloseRequested.emit(self.tabAt(event.pos()))


class CodeEditorTabWidget(QWidget):
    """
    Widget which representing code editor with tabs.
    """

    open_new_file = pyqtSignal(str)
    change_active_file = pyqtSignal(str)
    close_file = pyqtSignal(str)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        vertical_layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabBar(TabBar())
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setUsesScrollButtons(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.tab_changed)

        self.editor_status_bar = QStatusBar(self)
        self.editor_status_bar.setStyleSheet("QStatusBar{border-bottom: 1px outset grey; border-left: 1px outset grey; border-right: 1px outset grey;}")
        self.editor_status_bar.hide()

        vertical_layout.setSpacing(0)
        vertical_layout.setContentsMargins(5, 22, 0, 0)
        vertical_layout.addWidget(self.tab_widget)
        vertical_layout.addWidget(self.editor_status_bar)

        self.setLayout(vertical_layout)

        self.opened_tabs = 0
        self.opened_files = set()

        self.set_new_cursor_position_function = None

    def open_file(self, file_path: str) -> None:
        """
        Open file in new tab.

        Args:
            file_path(str): file path
        """
        if file_path in self.opened_files:
            self.change_current_tab(file_path)
            return

        with open(file_path, 'r') as f:
            code_editor = CodeEditorWidget(self)
            code_editor.load_file(f)
            code_editor.file_saved = True
            code_editor.opened_file = f.name
            code_editor.change_cursor_position.connect(self.set_new_cursor_position_function)
            self.add_tab(code_editor, os.path.basename(f.name))

        self.opened_files.add(file_path)
        self.open_new_file.emit(file_path)

    def new_file(self) -> None:
        """
        Create new tab / file
        """
        code_editor = CodeEditorWidget(self)
        code_editor.change_cursor_position.connect(self.set_new_cursor_position_function)
        code_editor.file_saved = False
        self.add_tab(code_editor, "NoName")

    def save_file(self, file_path: str = None) -> None:
        """
        Save current file(as).

        Args:
            file_path(str): if file path is not None. Save as method called
        """
        file = file_path or self.get_current_file()
        current_widget = self.get_current_widget()

        with open(file, 'w') as f:
            f.write(current_widget.get_plain_text())

        current_widget.opened_file = file
        current_widget.file_saved = True

        self.tab_changed()
        self.set_tab_text(os.path.basename(file))

    def add_tab(self, code_editor: CodeEditorWidget, file_name: str) -> None:
        """
        Add new tab to the widget.

        Args:
            code_editor(CodeEditorWidget): code editor widget in new tab
            file_name(str): name of new tab - file name
        """
        new_index = self.tab_widget.count()
        self.tab_widget.addTab(code_editor, file_name)
        self.tab_widget.setCurrentIndex(new_index)
        self.opened_tabs += 1

    def tab_changed(self) -> None:
        """
        Change hide/show information in editor status bar.
        Update line and column in main status bar.
        Set new active file in list widget.
        This method is called when currentChanged signal is emitted.
        """
        current_widget = self.get_current_widget()
        if not current_widget:
            self.editor_status_bar.hide()
            return
        else:
            self.editor_status_bar.showMessage(self.get_current_file() or "File not saved")
            self.editor_status_bar.show()

        current_widget.cursor_position_changed()

        self.change_active_file.emit(current_widget.opened_file)

    def set_tab_text(self, text: str, index: int = None) -> None:
        """
        Set new text of current tab

        Args:
            text(str): new text
            index(int): index of tab. If None -> use current
        """
        current_index = index or self.tab_widget.currentIndex()
        self.tab_widget.setTabText(current_index, text)

    def close_tab(self, index: int) -> None:
        """
        Close tab at index.

        Args:
            index(int): index of tab
        """
        file_path = self.tab_widget.widget(index).opened_file
        self.tab_widget.removeTab(index)
        self.opened_tabs -= 1
        self.close_file.emit(file_path)
        try:
            self.opened_files.remove(file_path)
        except KeyError:
            pass

    def is_file_saved(self) -> bool:
        """
        Return if file in current widget is saved.

        Returns:
            bool: True if file is save else False
        """
        current_tab = self.get_current_widget()
        return current_tab.file_saved

    def get_current_widget(self) -> CodeEditorWidget:
        """
        Return widget in current active tab

        Returns:
            CodeEditorWidget: Code editor in current tab
        """
        return self.tab_widget.currentWidget()

    def get_current_file(self) -> str:
        """
        Return file path of file in current active tab

        Returns:
            str: file path of file in active tab
        """
        return self.get_current_widget().opened_file

    def change_current_tab(self, file_path: str) -> None:
        """
        Change current active tab to tab with file_path file

        Args:
            file_path(str): file path
        """
        for idx in range(self.tab_widget.count()):
            if self.tab_widget.widget(idx).opened_file == file_path:
                self.tab_widget.setCurrentIndex(idx)
                break
