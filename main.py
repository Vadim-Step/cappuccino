import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class WindowDraw(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()
        self.pushButton.clicked.connect(self.run_2)
        self.pushButton_2.clicked.connect(self.run)

    def initUI(self):
        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()
        deal_cursor = cursor.execute(f'SELECT * FROM data')
        deals = [i for i in deal_cursor]
        if deals:
            self.tableWidget.setRowCount(0)
            for i in range(len(deals)):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for j in range(len(deals[i])):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(deals[i][j])))
        self.show()
        self.tableWidget.resizeColumnsToContents()

    def run(self):
        elem = [i.row() for i in self.tableWidget.selectedItems()]
        idd = self.tableWidget.item(elem[0], 0)
        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()
        deal_cursor = cursor.execute(f'SELECT * FROM data where id = {int(idd.text())}')
        deals = [i for i in deal_cursor]
        self.open_window(deals[0])

    def run_2(self):
        self.open_window_2()

    def open_window(self, deals):
        self.second_form = SecondForm(self, self.tableWidget, False, deals)
        self.second_form.show()

    def open_window_2(self):
        deals = ('', '', '', '', '', '')
        self.second_form = SecondForm(self, self.tableWidget, True, deals)
        self.second_form.show()


class SecondForm(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.args = args
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.run)
        if not self.args[-2]:
            self.lineEdit.setText(str(self.args[-1][1]))
            self.lineEdit_2.setText(str(self.args[-1][2]))
            self.lineEdit_3.setText(str(self.args[-1][3]))
            self.lineEdit_4.setText(str(self.args[-1][4]))
            self.lineEdit_5.setText(str(self.args[-1][5]))
            self.lineEdit_6.setText(str(self.args[-1][6]))

    def run(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        if not self.args[-2]:
            idd = self.args[-1][0]
            sort = self.lineEdit.text()
            roast = self.lineEdit_2.text()
            type = self.lineEdit_3.text()
            taste = self.lineEdit_4.text()
            cost = self.lineEdit_5.text()
            vol = self.lineEdit_6.text()
            cur.execute(
                """UPDATE data SET
                sort=?,
                roast=?,
                type=?,
                taste=?,
                cost=?,
                volume=?
                WHERE id=?""",
                (sort, roast, type, taste, cost, vol, idd)).fetchall()
        if self.args[-2]:
            sort = self.lineEdit.text()
            roast = self.lineEdit_2.text()
            type = self.lineEdit_3.text()
            taste = self.lineEdit_4.text()
            cost = self.lineEdit_5.text()
            vol = self.lineEdit_6.text()

            cur.execute(
                """INSERT INTO data(sort, roast, type, taste, cost, volume) VALUES(?, ?, ?, ? , ?, ?)""",
                (sort, roast, type, taste, cost, vol)).fetchall()
        con.commit()
        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()
        deal_cursor = cursor.execute(f'SELECT * FROM data')
        deals = [i for i in deal_cursor]
        self.tableWidget = self.args[1]
        if deals:
            self.tableWidget.setRowCount(0)
            for i in range(len(deals)):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for j in range(len(deals[i])):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(deals[i][j])))
        self.show()
        self.tableWidget.resizeColumnsToContents()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WindowDraw()
    ex.show()
    sys.exit(app.exec())
