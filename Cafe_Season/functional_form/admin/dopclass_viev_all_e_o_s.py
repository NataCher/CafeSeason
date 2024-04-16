from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
import sys
import psycopg2


from dopclass_add_employess import MainAdminAddEmployees
from dopclass_viev_order import MainAdminViewOrder
from dopclass_view_smene import MainAdminViewSmene



viev_employes_ui, _ = loadUiType('C:/Users/natal/Downloads/Cafe_Season/ui/forms/forms_admin/viev_employees.ui')
view_order_ui, _ = loadUiType('C:/Users/natal/Downloads/Cafe_Season/ui/forms/forms_admin/view_order.ui')
view_smene_ui, _ = loadUiType('C:/Users/natal/Downloads/Cafe_Season/ui/forms/forms_admin/view_smene.ui')
view_cook_ui, _ = loadUiType('C:/Users/natal/Downloads/Cafe_Season/ui/forms/forms_cook/view_orderc.ui')
order_ui, _ = loadUiType('C:/Users/natal/Downloads/Cafe_Season/ui/forms/forms_waiter/add_order_waiter.ui')
view_order_waiter_ui, _ = loadUiType('C:/Users/natal/Downloads/Cafe_Season/ui/forms/forms_waiter/view_order_waiter.ui')
Authorization_ui, _ = loadUiType('C:/Users/natal/Downloads/Cafe_Season/ui/Authorization.ui')
add_employees_ui, _ = loadUiType('C:/Users/natal/Downloads/Cafe_Season/ui/forms/forms_admin/add_employees.ui')
add_smene_ui, _ = loadUiType('C:/Users/natal/Downloads/Cafe_Season/ui/forms/forms_admin/add_smene.ui')




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


class MainAdminViewSmene(QMainWindow, view_smene_ui):
    def __init__(self, parent=None):
        super(MainAdminViewSmene, self).__init__(parent)

        self.setupUi(self)
        self.setFixedSize(self.size()) 
        self.setWindowIcon(QtGui.QIcon('C:/Users/natal/Downloads/Cafe_Season/static/img/Logotip.png'))   
        self.UpdateVievEmployees()

        self.table_smene.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_smene.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_smene.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.btn_order_empl.clicked.connect(self.OpenEmplo)
        self.btn_order_sm.clicked.connect(self.OpenOrder)
        self.btn_auth.clicked.connect(self.OpenAnth)
        self.btn_delete_sm.clicked.connect(self.DeleteSmene)
        self.btn_add_sm.clicked.connect(self.AddSmene)


    def UpdateViewSmene(self):
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="CafeSeason",
            user="postgres",
            password="nagashino"
        )

        cur = conn.cursor()

        cur.execute("SELECT s.id_s, e.firstname || ' ' || e.lastname || ' - ' || e.role, s.date, s.start, s.ending FROM smene s JOIN employee e ON s.id_employee = e.id_e")

        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:  
            return

        self.table_smene.setRowCount(len(rows))
        self.table_smene.setColumnCount(len(rows[0]))

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table_smene.setItem(i, j, item)
                item.setTextAlignment(Qt.AlignCenter)
            if rows:
                self.table_smene.setRowCount(len(rows))
                self.table_smene.setColumnCount(len(rows[0]))

    def DeleteSmene(self):
        selected_row = self.table_smene.currentRow()
        if selected_row != -1:
            smene_id = int(self.table_smene.item(selected_row, 0).text())
            conn = psycopg2.connect(
                host="127.0.0.1",
                database="CafeSeason",
                user="postgres",
                password="nagashino"
            )
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM smene WHERE id_s = %s", (smene_id,))
                conn.commit()

                QMessageBox.information(self, 'Кафе"Сезон"', 'Запись успешно удалена!')

                self.table_smene.removeRow(selected_row)

            except Exception as e:
                print("Ошибка при удалении смены:", e)
            finally:
                cur.close()
                conn.close()
        else:
            print("Ошибка: Не выбрана смена для удаления.")


    def AddSmene(self):
        self.close()
        self.addsmenes = MainAdminAddSmene()
        self.addsmenes.show()

    def OpenEmplo(self):
        self.close()
        self.open_empl = MainAdminEmployees()
        self.open_empl.show() 
   
    def OpenOrder(self):
        self.close()
        self.open_or = MainAdminViewOrder()
        self.open_or.show() 

    def OpenAnth(self):
        self.close()
        self.open_at_form = Authorization()
        self.open_at_form.show()


class MainAdminAddSmene(QMainWindow, add_smene_ui):
    def __init__(self, parent=None):
        super(MainAdminAddSmene, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size()) 
        self.setWindowIcon(QtGui.QIcon('C:/Users/natal/Downloads/Cafe_Season/static/img/Logotip.png'))  

        self.btn_save_smene.clicked.connect(self.SaveSmene)
        self.btn_back_smene.clicked.connect(self.OpenSmene)

        self.fill_combobox()

    def fill_combobox(self):
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="CafeSeason",
            user="postgres",
            password="nagashino"
        )
        cur = conn.cursor()

        try:
            cur.execute("SELECT firstname, lastname, role FROM employee")
            employees = cur.fetchall()
            for employee in employees:
                full_info = f"{employee[0]} {employee[1]} - {employee[2]}"  
                self.comboBox_empl.addItem(full_info)

        except Exception as e:
            print("Ошибка при получении данных из базы данных:", e)
        finally:
            cur.close()
            conn.close()

    def SaveSmene(self):
        selected_text = self.comboBox_empl.currentText()
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
                    shift_date = self.dt_date.text()
                    start_time = self.dt_start.text()
                    end_time = self.dt_end.text()

                    sql = """INSERT INTO smene (id_employee, date, start, ending)
                            VALUES (%s, %s, %s, %s)"""
                
                    cur.execute(sql, (employee_id, shift_date, start_time, end_time))
                    conn.commit()

                    print("Данные о смене успешно добавлены в базу данных.")
                else:
                    print("Ошибка: Сотрудник не найден в базе данных.")
            except Exception as e:
                print("Ошибка при добавлении данных о смене в базу данных:", e)
            finally:
                cur.close()
                conn.close()
        else:
            print("Ошибка: Не удалось разделить строку.")
            return

    def OpenSmene(self):
        self.close()
        self.opensmene_form = MainAdminViewSmene()
        self.opensmene_form.show()


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
        window = Authorization()
        window.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
        main()

