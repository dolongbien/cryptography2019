import sys
import os
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.uic import loadUi

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main.ui', self)
        self.title = "Cryptography and Network Security - Assignment 01"
        # self.top = 200
        # self.left = 400
        # self.width = 680
        # self.height = 480

        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)

        self.btnOpenFile.clicked.connect(self.openFile)
        self.btnOpenFolder.clicked.connect(lambda: self.openFile(True))
        self.show()

    @pyqtSlot()
    def openFile(self, isFolder = False):
        dialog = QFileDialog()
        if isFolder:
            dialog.setFileMode(QFileDialog.Directory)
        else:
            dialog.setFileMode(QFileDialog.AnyFile)

        fileNames = []
        if (dialog.exec()):
            fileNames = dialog.selectedFiles()
        if (fileNames):
            self.edtInput.setText(fileNames[0])

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())