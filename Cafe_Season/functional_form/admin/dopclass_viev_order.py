from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import psycopg2

view_order_ui, _ = loadUiType('C:/Users/natal/Downloads/Cafe_Season/ui/forms/forms_admin/view_order.ui')

class MainAdminViewOrder(QMainWindow, view_order_ui):
    def __init__(self, parent=None):
        super(MainAdminViewOrder, self).__init__(parent)

        self.setupUi(self)
        self.setFixedSize(self.size()) 
        self.setWindowIcon(QtGui.QIcon('C:/Users/natal/Downloads/Cafe_Season/static/img/Logotip.png'))
        
        self.UpdateTableOrder()

        self.table_order.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_order.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_order.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.btn_emp.clicked.connect(self.open_empl)
        self.btn_smene.clicked.connect(self.open_ord)
        self.btn_auth.clicked.connect(self.open_anth)

    def UpdateTableOrder(self):
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="CafeSeason",
            user="postgres",
            password="nagashino"
        )

        cur = conn.cursor()

     
        cur.execute("""
        SELECT s.id_o, e.firstname || ' ' || e.lastname || ' ' || e.patronymic AS id_employee, s."table_number", s.n_clients, s.dishes, s.drinks, s.status_w, s.status_o 
        FROM "orders" s 
        JOIN employee e ON s.id_employee = e.id_e
        WHERE e."role" = 'Официант'
    """)

        rows = cur.fetchall()
        cur.close()
        conn.close()

        self.table_order.setRowCount(len(rows))
        self.table_order.setColumnCount(8)

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.table_order.setItem(i, j, item)
                    item.setTextAlignment(Qt.AlignCenter)
               
    def open_empl(self):
        self.close()
        self.open_empl = MainAdminEmployees()
        self.open_empl.show() 

    def open_ord(self):
        self.close()
        self.open_o = MainAdminViewSmene()
        self.open_o.show() 

    def open_anth(self):
        self.close()
        self.open_at_form = Authorization()
        self.open_at_form.show()
  







def main():
    app = QApplication(sys.argv)
    window = MainAdminViewOrder()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
     main()
