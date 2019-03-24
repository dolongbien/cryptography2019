# -*- coding: utf-8 -*-
import hashlib
import os
import sys
import tarfile
import tempfile
from enum import Enum
from os.path import split
from allcipher import AllCipher
import time

# Import Qt modules
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtCore import QDateTime, Qt, QTimer
from Crypto.PublicKey import RSA

# Import the compiled UI module
# these modules are auto generated from .ui files designed in Qt Designer
from integrityCheckDialog import Ui_IntegrityCheckDialog
from rsa_ui import Ui_RSADialog
from window_ui import Ui_MainWindow
from key_ui import Ui_KeyDialog
import config
BOXTYPE = Enum('BoxType', 'SUCCESS ERROR')
SUCCESS_MESS = "Encrypted successfully in "

# Create a class for our main window
class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # This is always the same
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        config.process_bar.setRange(0,100)

    def add_file(self):
        """Add files or directories to the list of files/directories"""
            # select multiple files at a time
        filenames,_ = QFileDialog.getOpenFileNames(None, 'Select one or more files', './', None)
        self.ui.listWidget.addItems(filenames)
        if len(filenames)>0: # at least 1 file is selected
            self.ui.encryptButton.setEnabled(True)
        #self.ui.encryptButton.setEnabled(True)

    def remove_file(self):
        """Removes selected files (addresses) from the list"""
        listWidget = self.ui.listWidget
        selected = listWidget.selectedItems()
        for item in selected:
            row = listWidget.row(item)
            listWidget.takeItem(row)
            del item
        if listWidget.count() == 0:
            # if list is empty, remove and encrypt buttons disabled
            self.ui.removeButton.setEnabled(False)
            self.ui.encryptButton.setEnabled(False)

    def selection_changed(self):

        listWidget = self.ui.listWidget
        if listWidget.count() > 0:
            self.ui.removeButton.setEnabled(True)
        else:
            self.ui.removeButton.setEnabled(False)

    def encrypt(self):
        # reset progress bar
        config.process_bar.setValue(0)
        listWidget = self.ui.listWidget
        # open a dialog to choose/create file that will be our encrypted file
        filter = 'Encrypted (*.encrypted)'
        save_file = QFileDialog.getSaveFileName(self,
                                                'Save encrypted file',
                                                filter=filter)[0]
        tempfile = save_file + ".tmp"
        if save_file:
            # Making a tar archive from all files in the list and save tar as
            # chosen by user in file dialog
            with tarfile.open(tempfile, "w") as tar:
                for i in range(listWidget.count()):
                    item = listWidget.item(i).text()
                    tar.add(item, split(item)[1])
            # Getting password(key) for encryption
            if self.ui.rsa.isChecked():
                rsa_dialog = RSADlg(self)
                rsa_dialog.changeLabel("Public key: ")
                if rsa_dialog.exec_():
                    public_key = rsa_dialog.path()
                    cipher = AllCipher(str(public_key), save_file, isRSA=True)
                    start = time.time()
                    if cipher.encrypt_RSA():
                        config.process_bar.setValue(100)
                        end = time.time()
                        self.message_box(SUCCESS_MESS + str(round((end - start),3)) + " s")
                        os.remove(tempfile)
            else:
                pass_dialog = PasswordDlg(self)
                if pass_dialog.exec_():
                    password = pass_dialog.password()
                    cipher = AllCipher(str(password), save_file)
                    start = time.time()
                    # Encrypt ratio option: AES, DES
                    if self.ui.aes.isChecked():
                        if cipher.encrypt_AES():
                            config.process_bar.setValue(100)
                            end = time.time()
                            self.message_box(SUCCESS_MESS + str(round((end - start),3)) + " s")
                            os.remove(tempfile)
                    elif self.ui.des.isChecked():
                        if cipher.encrypt_DES():
                            config.process_bar.setValue(100)
                            end = time.time()
                            self.message_box(SUCCESS_MESS + str(round((end - start),3)) + " s")
                            os.remove(tempfile)

    def browse(self):
        self.encrypted_file = QFileDialog.getOpenFileNames(None, 'Please select encrypted file', './', None)[0] 
        # return a tuple, first is filename
        self.ui.lineEdit.setText(self.encrypted_file[0])

    def text_changed(self):
        if self.ui.lineEdit.text():
            self.ui.decryptButton.setEnabled(True)
        else:
            self.ui.decryptButton.setEnabled(False)

    def decrypt(self):
        # reset process bar
        config.process_bar.setValue(0)
        infile = self.ui.lineEdit.text()
        if not os.path.isfile(infile):
            self.message_box("File not found!")
            return

        outfile = False
        if self.ui.rsa.isChecked():
            rsa_dialog = RSADlg(self)
            rsa_dialog.changeLabel("Private key: ")
            if rsa_dialog.exec_():
                private_key = rsa_dialog.path()
                cipher = AllCipher(private_key, infile, isRSA=True)
                outfile = cipher.decrypt_RSA()
        else:
            pass_dialog = PasswordDlg(self)
            if pass_dialog.exec_():
                password = pass_dialog.password()
                cipher = AllCipher(password, infile)
                if self.ui.aes.isChecked():
                    outfile = cipher.decrypt_AES()
                elif self.ui.des.isChecked():
                    outfile = cipher.decrypt_DES()
        if outfile:
            config.process_bar.setValue(100)
            dir, fname = split(outfile)
            prefix = fname.rsplit('.tar', 1)[0]+' '
            outdir = tempfile.mkdtemp(prefix=prefix, dir=dir)
            with tarfile.open(outfile, 'r') as tar:
                tar.extractall(outdir)
            os.remove(outfile)
            self.message_box("Successful Decryption!")

    def integrityCheck(self):
        dialog = IntegrityDlg(self)
        if dialog.exec_():
            pass

    def message_box(self, text, type=BOXTYPE.SUCCESS):
        msgBox = QMessageBox()
        msgBox.setText(text)
        msgBox.setWindowTitle("BKU Encryption Tool")
        if type == BOXTYPE.SUCCESS:
            pixmap = QtGui.QPixmap(":/icon/image/check.png")
        elif type == BOXTYPE.ERROR:
            pixmap = QtGui.QPixmap(":/icon/image/delete.png")
        msgBox.setIconPixmap(pixmap)
        msgBox.exec_()

# inherit QDialog class
class PasswordDlg(QDialog):

    def __init__(self, parent=None, master=False):
        QDialog.__init__(self, parent=parent)

        # This is always the same
        self.ui = Ui_KeyDialog()
        self.ui.setupUi(self)

        ok_button = self.ui.buttonBox.button(QDialogButtonBox.Ok)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/image/check.png"),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ok_button.setIcon(icon)
        # adjust label if we are asking for master password
        if master:
            self.ui.label.setText("Enter Your Master Key:")
            self.setWindowTitle("Master Key")

    def password(self):
        return self.ui.lineEdit.text()

    def show_password(self):
        self.ui.lineEdit.setEchoMode(QLineEdit.Normal)

class RSADlg(QDialog):

    def __init__(self, parent=None, master=False):
        QDialog.__init__(self, parent=parent)

        # This is always the same
        self.ui = Ui_RSADialog()
        self.ui.setupUi(self)

        ok_button = self.ui.buttonBox.button(QDialogButtonBox.Ok)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/image/check.png"),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ok_button.setIcon(icon)

    def path(self):
        return self.ui.lineEdit.text()

    def changeLabel(self, content):
        self.ui.label.setText(content)

    def browse(self):
        self.key = QFileDialog.getOpenFileName()[0]
        self.ui.lineEdit.setText(self.key)

    def generate_key_RSA(self):
        filter = 'RSA Key (*.pem)'
        public_key = QFileDialog.getSaveFileName(self,
                                             'Save public key',
                                             filter=filter)[0]
        if public_key:
            private_key = QFileDialog.getSaveFileName(self,
                                                 'Save private key',
                                                 filter=filter)[0]
            if private_key:
                #Generate a public/ private key pair using 4096 bits key length (512 bytes)
                key = RSA.generate(4096)
                with open(public_key, "wb") as public:
                    with open(private_key, "wb") as private:
                        public.write(key.publickey().export_key("PEM"))
                        private.write(key.export_key("PEM"))
                        public.close()
                        private.close()

class IntegrityDlg(QDialog):

    def __init__(self, parent=None, master=False):
        QDialog.__init__(self, parent=parent)

        # This is always the same
        self.ui = Ui_IntegrityCheckDialog()
        self.ui.setupUi(self)

        ok_button = self.ui.btnVerify
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/image/check.png"),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ok_button.setIcon(icon)

    def browseOriginalFile(self):
        self.OriginalFile = QFileDialog.getOpenFileNames(None, 'Please select original file', './', None)[0]
        if self.OriginalFile:
            self.ui.edtOriginalFile.setText(self.OriginalFile[0])
            sha256_hash = hashlib.sha256()
            with open(self.OriginalFile[0], 'rb') as f:
                # Read and update hash string value in blocks of 4K
                for byte_block in iter(lambda: f.read(8192),b""):
                    sha256_hash.update(byte_block)
                self.hashOriginalFile = sha256_hash.hexdigest()
                self.ui.edtHashValueOriginalFile.setText(self.hashOriginalFile)

    def browseDecryptFile(self):
        self.DecryptFile = QFileDialog.getOpenFileNames(None, 'Please select decrypt file', './', None)[0]
        if self.DecryptFile:
            self.ui.edtDecryptFile.setText(self.DecryptFile[0])
            sha256_hash = hashlib.sha256()
            with open(self.DecryptFile[0], 'rb') as f:
                # Read and update hash string value in blocks of 4K
                for byte_block in iter(lambda: f.read(8192),b""):
                    sha256_hash.update(byte_block)
                self.hashDecryptFile = sha256_hash.hexdigest()
                self.ui.edtHashValueDecryptFile.setText(self.hashDecryptFile)

    def verify(self):
        if self.hashOriginalFile == self.hashDecryptFile:
            QMessageBox.information(self, "Integrity Check", "Integrity verificated!")
        else:
            QMessageBox.warning(self, "Integrity Check", "Integrity verification has failed")

def main():

    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
