# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pride/UI/opened_files_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OpenedFilesWidget(object):
    def setupUi(self, OpenedFilesWidget):
        OpenedFilesWidget.setObjectName("OpenedFilesWidget")
        OpenedFilesWidget.resize(393, 823)
        self.verticalLayout = QtWidgets.QVBoxLayout(OpenedFilesWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(OpenedFilesWidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setHandleWidth(0)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.tree_widget = QtWidgets.QTreeWidget(self.widget)
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setObjectName("tree_widget")
        self.tree_widget.headerItem().setText(0, "1")
        self.verticalLayout_2.addWidget(self.tree_widget)
        self.widget_2 = QtWidgets.QWidget(self.splitter)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.list_widget = QtWidgets.QListWidget(self.widget_2)
        self.list_widget.setObjectName("list_widget")
        self.verticalLayout_3.addWidget(self.list_widget)
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(OpenedFilesWidget)
        QtCore.QMetaObject.connectSlotsByName(OpenedFilesWidget)

    def retranslateUi(self, OpenedFilesWidget):
        _translate = QtCore.QCoreApplication.translate
        OpenedFilesWidget.setWindowTitle(_translate("OpenedFilesWidget", "Form"))
        self.label.setText(_translate("OpenedFilesWidget", "Directories"))
        self.label_2.setText(_translate("OpenedFilesWidget", "Files"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OpenedFilesWidget = QtWidgets.QWidget()
    ui = Ui_OpenedFilesWidget()
    ui.setupUi(OpenedFilesWidget)
    OpenedFilesWidget.show()
    sys.exit(app.exec_())
