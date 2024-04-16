from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import psycopg2


order_ui, _ = loadUiType('C:/Users/natal/Downloads/Cafe_Season/ui/forms/forms_waiter/add_order_waiter.ui')



class AddOrder(QMainWindow, order_ui):
    def __init__(self, parent=None):
        super(AddOrder, self).__init__(parent)

        self.setupUi(self)
        self.setFixedSize(self.size()) 
        self.setWindowIcon(QtGui.QIcon('C:/Users/natal/Downloads/Cafe_Season/static/img/Logotip.png'))   

        self.fill_combobox()

        self.btn_save.clicked.connect(self.SaveOrder)
        self.back_on_order.clicked.connect(self.OpenEmployee)


    def fill_combobox(self):
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="CafeSeason",
            user="postgres",
            password="nagashino"
        )
        cur = conn.cursor()

        try:
            cur.execute("SELECT firstname, lastname, role FROM employee WHERE role = 'Официант'")
            employees = cur.fetchall()
            for employee in employees:
                full_info = f"{employee[0]} {employee[1]} - {employee[2]}"  
                self.comboBox_add.addItem(full_info)

        except Exception as e:
            print("Ошибка при получении данных из базы данных:", e)
        finally:
            cur.close()
            conn.close()

    def SaveOrder(self):
        selected_text = self.comboBox_add.currentText()
        selected_text = selected_text.strip()  
        name_part, role_part = selected_text.rsplit('-', 1)  
        role_part = role_part.strip()

        if name_part and role_part:
            name_parts = name_part.split(' ')
            if len(name_parts) >= 2:
                first_name = name_parts[0]  
                last_name = ' '.join(name_parts[1:])  
            else:
                print("Ошибка: Недостаточно данных для разделения имени и фамилии.")
                return

            last_name = last_name.strip(' - ')
            role = role_part  

            conn = psycopg2.connect(
                host="127.0.0.1",
                database="CafeSeason",
                user="postgres",
                password="nagashino"
            )
            cur = conn.cursor()

            try:
                cur.execute("SELECT id_e FROM employee WHERE firstname = %s AND lastname = %s AND role = %s", (first_name, last_name, role))

                employee_record = cur.fetchone()
                print("Найденная запись в базе данных:", employee_record)
                if employee_record:  
                    employee_id = employee_record[0]  

                    line_table = self.le_table.text() or None
                    c_client = self.le_c_clients.text() or None
                    dishes = self.dishes_big.toPlainText() or None
                    drinks = self.drinks_big.toPlainText() 
                    st = self.le_status.text() 

                    sql = """INSERT INTO orders (id_employee, table_number, n_clients, dishes, drinks, status_w)
                            VALUES (%s, %s, %s, %s, %s, %s)"""

                    cur.execute(sql, (employee_id, line_table, c_client, dishes, drinks, st))
                    conn.commit()

                    QMessageBox.information(self, 'Кафе"Сезон"', 'Заказ добавлен!')
                    print("Данные о заказе успешно добавлены в базу данных.")
                else:
                    print("Ошибка: Сотрудник не найден в базе данных.")
            except Exception as e:
                print("Ошибка при добавлении данных о заказе в базу данных:", e)
            finally:
                cur.close()
                conn.close()

    def OpenEmployee(self):
        self.close()
        self.open_ord_form = MainVievOrderWaiter()
        self.open_ord_form.show() 






























        
def main():
    app = QApplication(sys.argv)
    window = AddOrder()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    
