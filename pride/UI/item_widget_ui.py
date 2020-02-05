# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pride/UI/item_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ItemWidget(object):
    def setupUi(self, ItemWidget):
        ItemWidget.setObjectName("ItemWidget")
        ItemWidget.resize(153, 36)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ItemWidget.sizePolicy().hasHeightForWidth())
        ItemWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ItemWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout.setContentsMargins(2, 4, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.file_name = QtWidgets.QLabel(ItemWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_name.sizePolicy().hasHeightForWidth())
        self.file_name.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.file_name.setPalette(palette)
        self.file_name.setText("")
        self.file_name.setObjectName("file_name")
        self.horizontalLayout.addWidget(self.file_name)
        self.file_path = QtWidgets.QLabel(ItemWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_path.sizePolicy().hasHeightForWidth())
        self.file_path.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.file_path.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.file_path.setFont(font)
        self.file_path.setText("")
        self.file_path.setObjectName("file_path")
        self.horizontalLayout.addWidget(self.file_path)

        self.retranslateUi(ItemWidget)
        QtCore.QMetaObject.connectSlotsByName(ItemWidget)

    def retranslateUi(self, ItemWidget):
        _translate = QtCore.QCoreApplication.translate
        ItemWidget.setWindowTitle(_translate("ItemWidget", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ItemWidget = QtWidgets.QWidget()
    ui = Ui_ItemWidget()
    ui.setupUi(ItemWidget)
    ItemWidget.show()
    sys.exit(app.exec_())
