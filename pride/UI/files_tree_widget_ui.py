# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pride/UI/files_tree_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_open_files_tree(object):
    def setupUi(self, open_files_tree):
        open_files_tree.setObjectName("open_files_tree")
        open_files_tree.resize(393, 823)
        self.verticalLayout = QtWidgets.QVBoxLayout(open_files_tree)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(open_files_tree)
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
        self.treeWidget = QtWidgets.QTreeWidget(self.widget)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.verticalLayout_2.addWidget(self.treeWidget)
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
        self.listWidget = QtWidgets.QListWidget(self.widget_2)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_3.addWidget(self.listWidget)
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(open_files_tree)
        QtCore.QMetaObject.connectSlotsByName(open_files_tree)

    def retranslateUi(self, open_files_tree):
        _translate = QtCore.QCoreApplication.translate
        open_files_tree.setWindowTitle(_translate("open_files_tree", "Form"))
        self.label.setText(_translate("open_files_tree", "Directories"))
        self.label_2.setText(_translate("open_files_tree", "Files"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    open_files_tree = QtWidgets.QWidget()
    ui = Ui_open_files_tree()
    ui.setupUi(open_files_tree)
    open_files_tree.show()
    sys.exit(app.exec_())
