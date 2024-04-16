from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
import sys
import psycopg2



view_smene_ui, _ = loadUiType('C:/Users/natal/Downloads/Cafe_Season/ui/forms/forms_admin/view_smene.ui')


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


    def UpdateVievEmployees(self):
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

def main():
        app = QApplication(sys.argv)
        window = MainAdminViewSmene()
        window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
     main()
        
