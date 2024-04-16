from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import psycopg2

add_smene_ui, _ = loadUiType('C:/Users/natal/Downloads/Cafe_Season/ui/forms/forms_admin/add_smene.ui')

class MainAdminAddSmene(QMainWindow, add_smene_ui):
    def __init__(self, parent=None):
        super(MainAdminAddSmene, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('C:/Users/natal/Downloads/Cafe_Season/static/img/Logotip.png'))  

        self.btn_save_smene.clicked.connect(self.save_smene)

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
                full_info = f"{employee[0]} {employee[1]} - {employee[2]}"  # Соединяем имя, фамилию и роль
                self.comboBox_empl.addItem(full_info)

        except Exception as e:
            print("Ошибка при получении данных из базы данных:", e)
        finally:
            cur.close()
            conn.close()

    def save_smene(self):
        # Получаем текст выбранного элемента из комбобокса
        selected_text = self.comboBox_empl.currentText()

        # Удаляем лишние пробелы в начале и в конце строки
        selected_text = selected_text.strip()

        # Разделяем строку на две части по последнему пробелу
        name_part, role_part = selected_text.rsplit('-', 1)  # Разделяем строку на имя/фамилию и роль

        # Убираем лишний пробел перед ролью
        role_part = role_part.strip()

        # Выводим отладочную информацию
        print("Запрос в базу данных:", name_part, role_part)

        # Убеждаемся, что были получены обе части
        if name_part and role_part:
            # Далее разделяем имя и фамилию
            name_parts = name_part.split(' ')
            if len(name_parts) >= 2:
                first_name = name_parts[0]  # Фамилия
                last_name = ' '.join(name_parts[1:])  # Имя - объединяем остальные части
            else:
                print("Ошибка: Недостаточно данных для разделения имени и фамилии.")
                return

            # Убираем дефис, если есть
            last_name = last_name.strip(' - ')
            role = role_part  # Роль

            conn = psycopg2.connect(
                host="127.0.0.1",
                database="CafeSeason",
                user="postgres",
                password="nagashino"
            )
            cur = conn.cursor()

            try:
                # Выбираем id сотрудника, основываясь на его имени, фамилии и роли
                cur.execute("SELECT id_e FROM employee WHERE firstname = %s AND lastname = %s AND role = %s", (first_name, last_name, role))
                employee_record = cur.fetchone()
                print("Найденная запись в базе данных:", employee_record)
                if employee_record:  # Проверяем, что запись сотрудника была найдена
                    employee_id = employee_record[0]  # Получаем идентификатор сотрудника

                    # Получаем дату и время начала и окончания смены
                    shift_date = self.dt_date.text()
                    start_time = self.dt_start.text()
                    end_time = self.dt_end.text()

                    # SQL-запрос для вставки данных в таблицу smene
                    sql = """INSERT INTO smene (id_employee, date, start, ending)
                            VALUES (%s, %s, %s, %s)"""
                    # Выполняем SQL-запрос с данными
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



def main():
    app = QApplication(sys.argv)
    window = MainAdminAddSmene()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
