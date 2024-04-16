from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import psycopg2

from dopclass_add_employess import MainAdminAddEmployees
from dopclass_viev_order import MainAdminViewOrder
from dopclass_view_smene import MainAdminViewSmene


viev_employes_ui, _ = loadUiType('C:/Users/natal/Downloads/Cafe_Season/ui/forms/forms_admin/viev_employees.ui')


class MainAdminEmployees(QMainWindow, viev_employes_ui):
    def __init__(self, parent=None):
        super(MainAdminEmployees, self).__init__(parent)

        self.setupUi(self)
        
        self.table_empl.setRowCount(0)

        self.setFixedSize(self.size()) 
        self.setWindowIcon(QtGui.QIcon('C:/Users/natal/Downloads/Cafe_Season/static/img/Logotip.png'))

        self.UpdateTableEmployees()


        self.table_empl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_empl.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_empl.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    
        self.table_empl.cellChanged.connect(self.UpdateEmployeeStatus)

        self.delete_empl.clicked.connect(self.DeleteEmployee)
        self.add_empl.clicked.connect(self.AddEmployees)
        self.btn_order.clicked.connect(self.OpenOrder)
        self.btn_smene.clicked.connect(self.OpenSmene)
        self.btn_auth.clicked.connect(self.OpenAnth)

        self.TableEditability()

    def UpdateTableEmployees(self):
 
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="CafeSeason",
            user="postgres",
            password="nagashino"
        )

        cur = conn.cursor()

        cur.execute("SELECT id_e, firstname, lastname, patronymic, role, status FROM employee")

        rows = cur.fetchall()
        cur.close()
        conn.close()

        self.table_empl.setRowCount(len(rows))
        self.table_empl.setColumnCount(len(rows[0]))

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table_empl.setItem(i, j, item)
                item.setTextAlignment(QtCore.Qt.AlignCenter)  

    def DeleteEmployee(self):
        selected_row = self.table_empl.currentRow()
        if selected_row != -1:
            employee_id = int(self.table_empl.item(selected_row, 0).text())
            conn = psycopg2.connect(
                host="127.0.0.1",
                database="CafeSeason",
                user="postgres",
                password="nagashino"
            )
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM employee WHERE id_e = %s", (employee_id,))
                conn.commit()

                print("Сотрудник успешно удален.")

                QMessageBox.information(self, 'Кафе"Сезон"', 'Запись удалена!')
                self.UpdateEmployeeStatus()  

            except Exception as e:
                print("Ошибка при удалении сотрудника:", e)
            finally:
                cur.close()
                conn.close()
        else:
            print("Ошибка: Не выбран сотрудник для удаления.")

    def AddEmployees(self):
        self.close()
        self.open_add_ = MainAdminAddEmployees()
        self.open_add_.show()       

    def TableEditability(self):
        for row in range(self.table_empl.rowCount()):
            for column in range(self.table_empl.columnCount()):
                if column != self.table_empl.columnCount() - 1: 
                    self.table_empl.item(row, column).setFlags(QtCore.Qt.ItemIsEnabled)  

    def UpdateEmployeeStatus(self, row, column):
        if column == 5:  
            item = self.table_empl.item(row, column)
            if item is not None and item.isSelected(): 
                employee_id = int(self.table_empl.item(row, 0).text())  
                new_status = item.text()  
                conn = psycopg2.connect(
                    host="127.0.0.1",
                    database="CafeSeason",
                    user="postgres",
                    password="nagashino"
                )
                cur = conn.cursor()
                try:
                    cur.execute("UPDATE employee SET status = %s WHERE id_e = %s", (new_status, employee_id))
                    conn.commit()

                    QMessageBox.information(self, 'Кафе"Сезон"', 'Статус сотрудника успешно обновлен!')

                except Exception as e:
                    print("Ошибка при обновлении статуса сотрудника:", e)
                finally:
                    cur.close()
                    conn.close()

    def OpenOrder(self):
        self.close()
        self.open_order_form = MainAdminViewOrder()
        self.open_order_form.show() 
        
    def OpenSmene(self):
        self.close()
        self.open_sm = MainAdminViewSmene()
        self.open_sm.show()  

    def OpenAnth(self):
        self.close()
        self.open_at_form = Authorization()
        self.open_at_form.show()

def main():
        app = QApplication(sys.argv)
        window = MainAdminEmployees()
        window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
     main()
        
