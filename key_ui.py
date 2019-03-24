# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'passwordDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_KeyDialog(object):
    def setupUi(self, KeyDialog):
        KeyDialog.setObjectName("KeyDialog")
        KeyDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        KeyDialog.resize(261, 138)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(KeyDialog.sizePolicy().hasHeightForWidth())
        KeyDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(KeyDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(KeyDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(KeyDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.label_show = QtWidgets.QLabel(KeyDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_show.sizePolicy().hasHeightForWidth())
        self.label_show.setSizePolicy(sizePolicy)
        self.label_show.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_show.setTextFormat(QtCore.Qt.AutoText)
        self.label_show.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse)
        self.label_show.setObjectName("label_show")
        self.verticalLayout.addWidget(self.label_show)
        spacerItem = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(KeyDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(KeyDialog)
        self.buttonBox.accepted.connect(KeyDialog.accept)
        self.buttonBox.rejected.connect(KeyDialog.reject)
        self.label_show.linkActivated['QString'].connect(KeyDialog.show_password)
        QtCore.QMetaObject.connectSlotsByName(KeyDialog)

    def retranslateUi(self, KeyDialog):
        _translate = QtCore.QCoreApplication.translate
        KeyDialog.setWindowTitle(_translate("KeyDialog", "Password"))
        self.label.setText(_translate("KeyDialog", "Enter Your Password:"))
        self.label_show.setText(_translate("KeyDialog", "<html><head/><body><p><a href=\"#\"><span style=\"color:#0000ff;\">Show Password</span></a></p></body></html>"))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    KeyDialog = QtWidgets.QDialog()
    ui = Ui_KeyDialog()
    ui.setupUi(KeyDialog)
    KeyDialog.show()
    sys.exit(app.exec_())

