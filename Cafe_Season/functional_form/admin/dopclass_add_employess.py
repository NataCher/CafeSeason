from PyQt5.QtCore import Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import psycopg2


add_employees_ui, _ = loadUiType('C:/Users/natal/Downloads/Cafe_Season/ui/forms/forms_admin/add_employees.ui')


class MainAdminAddEmployees(QMainWindow, add_employees_ui):
    def __init__(self, parent=None):
        super(MainAdminAddEmployees, self).__init__(parent)
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon('C:/Users/natal/Downloads/Cafe_Season/static/img/Logotip.png'))

        self.btn_back_empl.clicked.connect(self.open_employee)


        self.conn = psycopg2.connect(
            host="127.0.0.1",
            database="CafeSeason",
            user="postgres",
            password="nagashino"
        )

        self.btn_save_empl.clicked.connect(self.addEmployee)

        validator = QRegExpValidator(QRegExp("[A-Za-zА-Яа-яЁё]+"))
        self.first_name_line.setValidator(validator)

        validator = QRegExpValidator(QRegExp("[A-Za-zА-Яа-яЁё]+"))
        self.last_name_line.setValidator(validator)

        validator = QRegExpValidator(QRegExp("[A-Za-zА-Яа-яЁё]+"))
        self.patronymic_line.setValidator(validator)

    def addEmployee(self):
        cur = self.conn.cursor()
        firstName = self.first_name_line.text()
        lastName = self.last_name_line.text()
        patronymic = self.patronymic_line.text()
        role = self.role_combobox.currentText()
        status = self.status_combobox.currentText()

        fn = self.first_name_log.text()
        password = self.password_line.text()  

        sql = """INSERT INTO employee (firstName, lastName, patronymic, role, status)
                 VALUES (%s, %s, %s, %s, %s)"""
        
        sql2 = """INSERT INTO users (login, password, role)
                 VALUES (%s, %s, %s)"""

        try:
            cur.execute(sql, (firstName, lastName, patronymic, role, status))

            cur.execute(sql2, (fn, password, role))

            self.conn.commit()
            QMessageBox.information(self, 'Кафе "Сезон"', 'Сотрудник успешно добавлен в базу данных.')

            self.first_name_line.clear()
            self.last_name_line.clear()
            self.patronymic_line.clear()
            self.role_combobox.setCurrentIndex(0)
            self.status_combobox.setCurrentIndex(0)


        except psycopg2.Error as e:
            QMessageBox.warning(self, 'Кафе "Сезон"', 'Ошибка при добавлении сотрудника в базу данных:\n{}'.format(e))
        
        cur.close()

    def open_employee(self):
        self.close()
        self.open_empl_form = MainAdminEmployees()
        self.open_empl_form.show()



def main():
        app = QApplication(sys.argv)
        window = MainAdminAddEmployees()
        window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
     main()
        
