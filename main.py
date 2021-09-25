from Save import Ui_Form
import sys
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget, QLineEdit,
                             QRadioButton,QCommandLinkButton, QMessageBox, QInputDialog)
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QProcess

from cryptography.fernet import Fernet

import csv

PW = {} # Dict for PW


def write_key():
    try:
        return open("key.key", "rb").read()
    except:
        key= Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)

        return open("key.key", "rb").read()

# ----------------------------------------------
# crypt-----------------------------------------

def encrypy(st, key):
    f=Fernet(key)

    with open(st, "rb") as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)

    with open(st, "wb") as file:
        file.write(encrypted_data)

def decrypt(st, key):
    f = Fernet(key)
    with open(st, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = f.decrypt(encrypted_data)

    with open(st,"wb") as file:
        file.write(decrypted_data)

# --------------------------------------------------
# main----------------------------------------------

class Window(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.init()
        key = write_key()
        print(key)

    def loadPW(self):
        global PW
        self.PWListWidget.clear()
        with open('pw.csv', mode='r') as infile:
            reader = csv.reader(infile)
            for rows in reader:
                if len(rows) < 1:
                    continue
                else:
                    PW[rows[0]] = (rows[1], rows[2])
                    self.PWListWidget.addItem(rows[0])

    def Changeecho(self, enabled):  # show Password or not
        if not enabled:
            self.PWlineEdit.setEchoMode(QLineEdit.Normal)
            self.print()
        else:
            self.PWlineEdit.setEchoMode(QLineEdit.Password)

    def Save(self):

        if self.PWListWidget.count() >= 1:
            for index in range(self.PWListWidget.count()):
                if self.PWListWidget.item(index).text() == self.WebLineEdit.text():
                    check = True
                    break

                else:
                    check = False

            if check == False:
                self.PWListWidget.addItem(self.WebLineEdit.text())
                PW[self.WebLineEdit.text()] = self.IDlineEdit.text(), self.PWlineEdit.text()
                w = csv.writer(open("pw.csv", "w"))
                for key, val in PW.items():
                    w.writerow([key, val[0], val[1]])



            else:
                self.msgbox()

        else:
            self.PWListWidget.addItem(self.WebLineEdit.text())
            PW[self.WebLineEdit.text()] = self.IDlineEdit.text(), self.PWlineEdit.text()
            w = csv.writer(open("pw.csv", "w"))
            for key, val in PW.items():
                w.writerow([key, val[0], val[1]])
                print(val[0])
                print(val[1])


    def msgbox(self):
        btn = QMessageBox.question(self, "Same name detected", "Do you want to overwrite it?", QMessageBox.Yes | QMessageBox.No)
        if btn == QMessageBox.Yes:
            PW.update({self.WebLineEdit.text() : (self.IDlineEdit.text(), self.PWlineEdit.text())})
            w = csv.writer(open("pw.csv", "w"))
            for key, val in PW.items():
                w.writerow([key, val[0], val[1]])
                print(val[0])
                print(val[1])
        else:
            pass

    def decrypt(self):
        decrypt('pw.csv', write_key())

    def encrypt(self):
        encrypy('pw.csv', write_key())



    def print(self):
        print(PW)

    def pwbox(self, item):
        x = PW[item.text()]
        url = item.text()
        id = x[0]
        pw = x[1]
        print(id)
        print(pw)
        self.WebLineEdit.setText(url)
        self.IDlineEdit.setText(id)
        self.PWlineEdit.setText(pw)

    def init(self):
        self.loadPW()
        self.loadButton.clicked.connect(self.loadPW)
        self.PWhidebutton.toggled.connect(self.Changeecho)
        self.SaveButton.clicked.connect(self.Save)
        self.PWListWidget.itemClicked.connect(self.pwbox)
        self.EncryptButton.clicked.connect(self.encrypt)
        self.DecryptButton.clicked.connect(self.decrypt)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())