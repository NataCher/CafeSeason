from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import psycopg2

from dopclass_add_order import AddOrder

view_order_waiter_ui, _ = loadUiType('C:/Users/natal/Downloads/Cafe_Season/ui/forms/forms_waiter/view_order_waiter.ui')


class MainVievOrderWaiter(QMainWindow, view_order_waiter_ui):
    def __init__(self, parent=None):
        super(MainVievOrderWaiter, self).__init__(parent)

        self.setupUi(self)
        self.setFixedSize(self.size()) 
        self.setWindowIcon(QtGui.QIcon('C:/Users/natal/Downloads/Cafe_Season/static/img/Logotip.png')) 

        self.UpdateTableOrder()
        self.TableEditability()
  

        self.table_order.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_order.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_order.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
       
        self.btn_add_order.clicked.connect(self.OpenAddOrder) 
        self.table_order.cellChanged.connect(self.UpdateOrderStatus)
        self.btn_auth.clicked.connect(self.OpenAnth)
        self.btn_delete_order.clicked.connect(self.DeleteOrder)

    def TableEditability(self):
       
        for row in range(self.table_order.rowCount()):
            for column in range(self.table_order.columnCount()):
                item = self.table_order.item(row, column)
                if item is not None:  
                    if column != self.table_order.columnCount() - 2: 
                        item.setFlags(QtCore.Qt.ItemIsEnabled)

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

        if rows:  
            self.table_order.setRowCount(len(rows))
            self.table_order.setColumnCount(len(rows[0]))

            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.table_order.setItem(i, j, item)
                    item.setTextAlignment(Qt.AlignCenter)
        else:
                self.table_order.setRowCount(0) 
                self.table_order.setColumnCount(0)  

    def OpenAddOrder(self):
        self.close()
        self.add_order_form = AddOrder()
        self.add_order_form.show()

    def DeleteOrder(self):
        selected_row = self.table_order.currentRow()
        if selected_row != -1:
            id_o = int(self.table_order.item(selected_row, 0).text())
            conn = psycopg2.connect(
                host="127.0.0.1",
                database="CafeSeason",
                user="postgres",
                password="nagashino"
            )
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM orders WHERE id_o = %s", (id_o,))
                conn.commit()
                QMessageBox.information(self, 'Кафе"Сезон"', 'Заказ удален!')  
                self.table_order.blockSignals(True)
                self.UpdateTableOrder()  
                self.table_order.blockSignals(False)
            except Exception as e:
                print("Ошибка при удалении сотрудника:", e)
            finally:
                cur.close()
                conn.close()
        else:
            print("Ошибка: Не выбран заказ для удаления.")


    def UpdateOrderStatus(self, row, column):
        if column == 6:  
            order_id = int(self.table_order.item(row, 0).text())  
            new_status = self.table_order.item(row, column).text()  
            conn = psycopg2.connect(
                host="127.0.0.1",
                database="CafeSeason",
                user="postgres",
                password="nagashino"
            )
            cur = conn.cursor()
            try:
                cur.execute("UPDATE orders SET status_w = %s WHERE id_o = %s", (new_status, order_id))
                conn.commit()
                QMessageBox.information(self, 'Кафе"Сезон"', 'Статус заказа успешно обновлен!')
          
            except Exception as e:
                print("Ошибка при обновлении статуса заказа:", e)
            finally:
                cur.close()
                conn.close()

    def OpenAddOrder(self):
        self.close()
        self.add_order_form = AddOrder()
        self.add_order_form.show()

    def OpenAnth(self):
        self.close()
        self.open_at_form = Authorization()
        self.open_at_form.show()  


def main():
    app = QApplication(sys.argv)
    window = MainVievOrderWaiter()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    
