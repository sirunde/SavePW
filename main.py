from Save import Ui_Form
import sys
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget, QLineEdit,
                             QRadioButton,QCommandLinkButton, QMessageBox, QInputDialog)
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QProcess

from cryptography.fernet import Fernet

import csv

PW = {} # Dict for PW

# generate key
# ------------------------------------------------
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
        print(file_data)

    encrypted_data = f.encrypt(file_data)

    with open(st, "wb") as file:
            file.write(encrypted_data)

def decrypt(st, key):
    f = Fernet(key)

    with open(st, "rb") as file:
        encrypted_data = file.read()

        if len(encrypted_data) >= 1:
            decrypted_data = f.decrypt(encrypted_data)
            pass

        else:
            decrypted_data = encrypted_data
            pass

    file.close()

    with open(st, "wb") as file:
        file.write(decrypted_data)

    file.close()

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

        decrypt('pw.csv', write_key())

        with open('pw.csv', mode='r') as infile:
            reader = csv.reader(infile)
            for rows in reader:
                if len(rows) < 1:
                    continue
                else:

                    PW[rows[0]] = (rows[1], rows[2])
                    self.PWListWidget.addItem(rows[0])

        encrypy('pw.csv', write_key())


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
                    check = True # password is already in list
                    break

                else:
                    check = False # password is not in list

            if check == False:
                self.PWListWidget.addItem(self.WebLineEdit.text())
                PW[self.WebLineEdit.text()] = self.IDlineEdit.text(), self.PWlineEdit.text()
                decrypt('pw.csv', write_key())
                print("decrypted")
                w = csv.writer(open("pw.csv", "w"))
                for key, val in PW.items():
                    w.writerow([key, val[0], val[1]])

                w = None

                print(PW)

                encrypy('pw.csv', write_key())
                print("encrypted")




            else:
                self.msgbox()

        else:
            self.PWListWidget.addItem(self.WebLineEdit.text())
            PW[self.WebLineEdit.text()] = self.IDlineEdit.text(), self.PWlineEdit.text()
            w = csv.writer(open("pw.csv", "w"))
            for key, val in PW.items():
                w.writerow([key, val[0], val[1]])
            w = None

            encrypy('pw.csv', write_key())
            print("encrypted")

    def msgbox(self):
        btn = QMessageBox.question(self, "Same name detected", "Do you want to overwrite it?", QMessageBox.Yes | QMessageBox.No)
        if btn == QMessageBox.Yes:
            PW.update({self.WebLineEdit.text() : (self.IDlineEdit.text(), self.PWlineEdit.text())})
            decrypt('pw.csv', write_key())
            print("decrypted")

            w = csv.writer(open("pw.csv", "w"))
            for key, val in PW.items():
                w.writerow([key, val[0], val[1]])
                print(val[0])
                print(val[1])

            w = None

            encrypy('pw.csv', write_key())

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