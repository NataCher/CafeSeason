from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import psycopg2

view_cook_ui, _ = loadUiType('C:/Users/natal/Downloads/Cafe_Season/ui/forms/forms_cook/view_orderc.ui')

class CookViewOrder(QMainWindow, view_cook_ui):
    def __init__(self, parent=None):
        super(CookViewOrder, self).__init__(parent)

        self.setupUi(self)
        self.setFixedSize(self.size()) 
        self.setWindowIcon(QtGui.QIcon('C:/Users/natal/Downloads/Cafe_Season/static/img/Logotip.png'))   

        self.UpdateTableOrder()

        self.table_order.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_order.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_order.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.btn_save_status.clicked.connect(self.UpdateStatus)
        self.btn_auth.clicked.connect(self.OpenAnth)

        self.SetTableEdit()

    def UpdateTableOrder(self):
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="CafeSeason",
            user="postgres",
            password="nagashino"
        )

        cur = conn.cursor()

        cur.execute("""
           SELECT s.id_o, e.firstname || ' ' || e.lastname ||' '|| e.patronymic , s."table_number", s.n_clients, s.dishes, s.drinks, s.status_w, s.status_o 
            FROM "orders" s 
            JOIN employee e ON s.id_employee = e.id_e 
            WHERE e."role" = 'Официант'
        """)

        rows = cur.fetchall()
        cur.close()
        conn.close()

        self.table_order.setRowCount(len(rows))
        self.table_order.setColumnCount(7)

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table_order.setItem(i, j, item)
                item.setTextAlignment(Qt.AlignCenter)

    def UpdateStatus(self):
        selected_row = self.table_order.currentRow()  
        column = 6  
        item = self.table_order.item(selected_row, 0)  
        order_id = int(item.text()) 
        new_status = self.table_order.item(selected_row, column).text()  
        
        self.UpdateOrderStatus(order_id, new_status)
    
    def UpdateOrderStatus(self, order_id, new_status):
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="CafeSeason",
            user="postgres",
            password="nagashino"
        )
        cur = conn.cursor()
        try:
            cur.execute("UPDATE orders SET status_o = %s WHERE id_o = %s", (new_status, order_id))
            conn.commit()
            QMessageBox.information(self, 'Кафе"Сезон"', 'Статус заказа успешно обновлен!')
        except Exception as e:
            print("Ошибка при обновлении статуса заказа:", e)
        finally:
            cur.close()
            conn.close()

    def SetTableEdit(self):  
        for row in range(self.table_order.rowCount()):
            for column in range(self.table_order.columnCount()):
                if column != self.table_order.columnCount() - 1:  
                    self.table_order.item(row, column).setFlags(QtCore.Qt.ItemIsEnabled)  

    def OpenAnth(self):
        self.close()
        self.open_at_form = Authorization()
        self.open_at_form.show()  

def main():
    app = QApplication(sys.argv)
    window = CookViewOrder()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
