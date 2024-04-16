from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import pandas as pd
import psycopg2
from PyQt5.uic import loadUiType

from functional_form.admin.dopclass_viev_all_e_o_s import MainAdminEmployees, CookViewOrder, MainVievOrderWaiter



Authorization_ui, _ = loadUiType('C:/Users/natal/Downloads/Cafe_Season/ui/Authorization.ui')


class Authorization(QMainWindow, Authorization_ui):
    def __init__(self, parent=None):
        super(Authorization, self).__init__(parent)
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon('C:/Users/natal/Downloads/Cafe_Season/static/img/Logotip.png'))       
      
        self.pushButton.clicked.connect(self.login)
        self.setFixedSize(self.size())  


    def login(self):
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()
        role = self.comboBox.currentText()
        try:
            connection = psycopg2.connect(
                    host="127.0.0.1",
                    database="CafeSeason",
                    user="postgres",
                    password="nagashino"  
            )
            cursor = connection.cursor()
            
            cursor.execute("SELECT * FROM users WHERE login = %s AND password = %s AND role = %s", (login, password, role))

            user = cursor.fetchone()
            
            if user:   
                if role == "Администратор":
                    self.close()
                    self.ve_admin = MainAdminEmployees()
                    self.ve_admin.show()
                elif role == "Официант":
                    self.close()
                    self.vo_waiter = MainVievOrderWaiter()
                    self.vo_waiter.show()
                elif role == "Повар":
                    self.close()
                    self.vo_admin = CookViewOrder()
                    self.vo_admin.show()

            else:
                QMessageBox.warning(self, "Ошибка", "Неправильный логин или пароль")
        
        except (Exception, psycopg2.Error) as error:
            print("Ошибка при работе с PostgreSQL", error)



def main():
        app = QApplication(sys.argv)
        window = Authorization()
        window.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
        main()

