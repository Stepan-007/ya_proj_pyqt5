import sqlite3
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
import sys
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=1, height=2, dpi=50):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class DBSample(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('qt_proj4.ui', self)
        self.params = {'Сортировка по году': 'year',
                       'Сортировка по месяцу': 'month'}
        self.con = sqlite3.connect(self.input.text())
        self.poisk.clicked.connect(self.Do)
        self.clear.clicked.connect(self.clear_all)
        self.gr_bild.clicked.connect(self.build_graph)
        self.res = []
        self.months = ['январь',
                       'февраль',
                       'март',
                       'апрель',
                       'май',
                       'июнь',
                       'июль',
                       'август',
                       'сентябрь',
                       'октябрь',
                       'ноябрь',
                       'декабрь']

    def build_graph(self):  # построение графика
        con = sqlite3.connect(self.input.text())
        cur = con.cursor()
        try:
            if not self.input.text():
                self.Error_2.setText('Вы не ввели имя файла')
                return
            try:
                if not self.para_poisk.text():
                    sc = MplCanvas(self, width=3, height=3, dpi=65)
                    res_x = []
                    res_y = []
                    self.verticalLayout.addWidget(sc)

                    x = cur.execute(f"""SELECT спрос FROM test""").fetchall()
                    for i in x:
                        res_x.append(i[0])
                    res_x.sort(reverse=True)
                    y = cur.execute(f"""SELECT month FROM test""").fetchall()
                    for j in y:
                        res_y.append(j[0])
                    res_y.sort(reverse=True)
                    sc.axes.plot(res_x, res_y)
                    self.show()
                try:
                    if self.para_poisk.text().isdigit():
                        sc = MplCanvas(self, width=3, height=3, dpi=65)
                        res_x = []
                        res_y = []
                        self.verticalLayout.addWidget(sc)

                        x = cur.execute(
                            f"""SELECT спрос FROM test WHERE year = {self.para_poisk.text()}""").fetchall()
                        for i in x:
                            res_x.append(i[0])
                        res_x.sort(reverse=True)
                        y = cur.execute(
                            f"""SELECT month FROM test WHERE year = {self.para_poisk.text()}""").fetchall()
                        for j in y:
                            res_y.append(j[0])
                        res_y.sort(reverse=True)
                        sc.axes.plot(res_x, res_y)
                        self.show()
                    if self.para_poisk.text() in self.months:
                        sc = MplCanvas(self, width=3, height=3, dpi=65)
                        res_x = []
                        res_y = []
                        self.verticalLayout.addWidget(sc)
                        s = f"""SELECT cпрос FROM test WHERE month = '{self.para_poisk.text()}'"""
                        x = cur.execute(s).fetchall()
                        for i in x:
                            res_x.append(i[0])
                        res_x.sort(reverse=True)
                        y = cur.execute(
                            f"""SELECT date FROM test WHERE month = '{self.para_poisk.text()}'""").fetchall()
                        for j in y:
                            res_y.append(j[0])
                        res_y.sort(reverse=True)
                        sc.axes.plot(res_x, res_y)
                        self.show()
                except FileNotFoundError or sqlite3.OperationalError or sqlite3.DatabaseError:
                    self.Error_1.setText('Файле не найден/Ошибка базы данных')
            except FileNotFoundError or sqlite3.OperationalError or sqlite3.DatabaseError:
                self.Error_1.setText('Файле не найден/Ошибка базы данных')
        except FileNotFoundError or sqlite3.OperationalError or sqlite3.DatabaseError:
            self.Error_1.setText('Файл не найден/Не верный формат базы данных')

    def Do(self):  # нахождение максимума и минимама в базе данных
        try:
            if not self.input.text():
                self.Error_2.setText('Вы не ввели имя файла')
                return
            try:
                if not self.para_poisk.text():
                    self.Error_2.setText('Вы не указали параметр отбора/Отбор прозойдет без параметра')
                    con = sqlite3.connect(self.input.text())
                    cur = con.cursor()
                    name_file = f"""SELECT спрос FROM test"""
                    res = cur.execute(name_file).fetchall()
                    new_res = []
                    for i in res:
                        new_res.append(i[0])
                    summa = sum(new_res)
                    max_spros = max(new_res)
                    min_spros = min(new_res)
                    max_month = cur.execute(
                        f"""SELECT month FROM test WHERE спрос = {max_spros}""").fetchall()
                    min_month = cur.execute(
                        f"""SELECT month FROM test WHERE спрос = {max_spros}""").fetchall()
                    max_month_ch = cur.execute(
                        f"""SELECT year FROM test WHERE спрос = {max_spros}""").fetchall()
                    month = []
                    min_month_ch = cur.execute(
                        f"""SELECT year FROM test WHERE спрос = {min_spros}""").fetchall()

                    for i in max_month:
                        for j in max_month_ch:
                            self.month.setText(str(i[0]) + ' ' + str(j[0]))
                    for i in min_month:
                        for j in min_month_ch:
                            self.month_2.setText(str(i[0]) + ' ' + str(j[0]))
                    self.month_ch.setText(str(max_spros))
                    self.month_min_ch.setText(str(min_spros))
                    self.summa.setText(str(summa))
                    self.colvo_il.setText(str(len(new_res)))
                    return
                con = sqlite3.connect(self.input.text())
                cur = con.cursor()

                req = "SELECT * FROM test WHERE {} = '{}'".format(self.params.get(self.combo_years.currentText()),
                                                                  self.para_poisk.text())
                print(req)
                print(self.params.get(self.combo_years.currentText()), self.para_poisk.text())
                res = cur.execute(req).fetchone()
                print(res)
                if not res:
                    self.Error_1.setText('Ничего не найдено')
                    self.month.setText('')
                    self.month_ch.setText('')
                    self.month_2.setText('')
                    self.month_min_ch.setText('')
                    self.summa.setText('')
                    self.colvo_il.setText('')
                    return
                try:
                    if self.para_poisk.text() in self.months:
                        name_file = f"""SELECT спрос FROM test WHERE month = '{self.para_poisk.text()}'"""
                        res = cur.execute(name_file).fetchall()
                        new_res = []
                        print(res)
                        for i in res:
                            new_res.append(i[0])
                        # print(new_res)
                        max_spros = max(new_res)
                        min_spros = min(new_res)
                        summa = sum(new_res)
                        max_month_ch = cur.execute(
                            f"""SELECT year FROM test WHERE спрос = {max_spros}""").fetchall()
                        month = []
                        min_month_ch = cur.execute(
                            f"""SELECT year FROM test WHERE спрос = {min_spros}""").fetchall()
                        for j in max_month_ch:
                            self.month.setText(str(self.para_poisk.text()) + ' ' + str(j[0]))
                        for j in min_month_ch:
                            self.month_2.setText(str(self.para_poisk.text()) + ' ' + str(j[0]))
                        self.month_ch.setText(str(max_spros))
                        self.month_min_ch.setText(str(min_spros))
                        self.summa.setText(str(summa))
                        self.colvo_il.setText(str(len(new_res)))
                    if self.para_poisk.text().isdigit():
                        name_file = f"""SELECT спрос FROM test WHERE year = {self.para_poisk.text()}"""
                        res = cur.execute(name_file).fetchall()
                        new_res = []
                        print(res)
                        for i in res:
                            new_res.append(i[0])
                        max_spros = max(new_res)
                        min_spros = min(new_res)
                        summa = sum(new_res)
                        max_month = cur.execute(
                            f"""SELECT month FROM test WHERE спрос = {max_spros}""").fetchall()
                        month = []
                        min_month = cur.execute(
                            f"""SELECT month FROM test WHERE спрос = {min_spros}""").fetchall()
                        mi_month = []
                        for i in max_month:
                            self.month.setText(str(i[0]))
                        for i in min_month:
                            self.month_2.setText(str(i[0]))
                        self.month_ch.setText(str(max_spros))
                        self.month_min_ch.setText(str(min_spros))
                        self.summa.setText(str(summa))
                        self.colvo_il.setText(str(len(new_res)))

                except FileNotFoundError or sqlite3.OperationalError or sqlite3.DatabaseError:
                    self.Error_1.setText('Не верный формат базы данных')
            except FileNotFoundError or sqlite3.OperationalError or sqlite3.DatabaseError:
                self.Error_1.setText('Файл не найден/Не верный формат базы данных')
        except FileNotFoundError or sqlite3.OperationalError or sqlite3.DatabaseError:
            self.Error_1.setText('Файл не найден/Не верный формат базы данных')

    def clear_all(self):  # Функция для очищения всех полей
        self.month.setText('')
        self.month_ch.setText('')
        self.month_2.setText('')
        self.month_min_ch.setText('')
        self.para_poisk.setText('')
        self.Error_1.setText('')
        self.Error_2.setText('')
        self.summa.setText('')
        self.colvo_il.setText('')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    app.exec_()
    sys.excepthook = except_hook
    sys.exit(app.exec())
