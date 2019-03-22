# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rsaDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RSADialog(object):
    def setupUi(self, RSADialog):
        RSADialog.setObjectName("RSADialog")
        RSADialog.setWindowModality(QtCore.Qt.ApplicationModal)
        RSADialog.resize(350, 217)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RSADialog.sizePolicy().hasHeightForWidth())
        RSADialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(RSADialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(RSADialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(RSADialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        # self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(RSADialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_show = QtWidgets.QLabel(RSADialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_show.sizePolicy().hasHeightForWidth())
        self.label_show.setSizePolicy(sizePolicy)
        self.label_show.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_show.setTextFormat(QtCore.Qt.AutoText)
        self.label_show.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse)
        self.label_show.setObjectName("label_show")
        self.horizontalLayout_4.addWidget(self.label_show)
        self.pushButtonGenkey = QtWidgets.QPushButton(RSADialog)
        self.pushButtonGenkey.setObjectName("pushButtonGenkey")
        self.horizontalLayout_4.addWidget(self.pushButtonGenkey)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        spacerItem = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(RSADialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(RSADialog)
        self.buttonBox.accepted.connect(RSADialog.accept)
        self.buttonBox.rejected.connect(RSADialog.reject)
        self.pushButton.clicked.connect(RSADialog.browse)
        self.pushButtonGenkey.clicked.connect(RSADialog.generate_key_RSA)
        self.label_show.linkActivated['QString'].connect(RSADialog.generate_key_RSA)
        QtCore.QMetaObject.connectSlotsByName(RSADialog)

    def retranslateUi(self, RSADialog):
        _translate = QtCore.QCoreApplication.translate
        RSADialog.setWindowTitle(_translate("RSADialog", "RSA"))
        self.label.setText(_translate("RSADialog", "Enter Your RSA key:"))
        self.pushButton.setText(_translate("RSADialog", "browse"))
        self.label_show.setText(_translate("RSADialog", "<html><head/><body><p><a href=\"#\"><span style=\" text-decoration: underline; color:#0000ff;\">Not have key for RSA algorithm?</span></a></p></body></html>"))
        self.pushButtonGenkey.setText(_translate("RSADialog", "Generate key"))

import resources_rc
