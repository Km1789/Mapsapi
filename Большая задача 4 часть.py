import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

SCREEN_SIZE = [720, 450]
spn = (0.002, 0.002)
ll = (37.530887, 55.703118)
l = "map"


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def keyPressEvent(self, event):
        global spn, ll, l
        if event.key() == Qt.Key_PageDown:
            spn = (spn[0] + 0.02, spn[1] + 0.02)
            if spn[0] > 10 or spn[1] > 10:
                spn = (10, 10)
            print(spn)
            self.update()

        if event.key() == Qt.Key_PageUp:
            spn = (spn[0] - 0.02, spn[1] - 0.02)
            if spn[0] < 0.001 or spn[1] < 0.001:
                spn = (0.001, 0.001)
            print(spn)
            self.update()

        if event.key() == Qt.Key_Up:
            q = ll[1] - (0.6 * spn[1])
            c = "%.6f" % q
            ll = (ll[0], float(c))
            if ll[0] < 0 or ll[1] < 0:
                ll = (1, 1)
            print(ll)
            self.update()

        if event.key() == Qt.Key_Down:
            q = ll[1] + (0.6 * spn[1])
            c = "%.6f" % q
            ll = (ll[0], float(c))
            if ll[0] > 90 or ll[1] > 90:
                ll = (80, 80)
            print(ll)
            self.update()

        if event.key() == Qt.Key_Left:
            q = ll[0] + (1.5 * spn[0])
            c = "%.6f" % q
            ll = (float(c), ll[1])
            if ll[0] > 90 or ll[1] > 90:
                ll = (80, 80)
            print(ll)
            self.update()

        if event.key() == Qt.Key_Right:
            q = ll[0] - (1.5 * spn[0])
            c = "%.6f" % q
            ll = (float(c), ll[1])
            if ll[0] < 0 or ll[1] < 0:
                ll = (1, 1)
            print(ll)
            self.update()

    def update(self):
        self.getImage()
        self.image.clear()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={str(ll[0])},{str(ll[1])}&spn={str(spn[0])},{str(spn[1])}&l={l}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

        self.map = QPushButton('Карта', self)
        self.map.move(620, 150)
        self.map.resize(80, 30)
        self.map.clicked.connect(self.map_func)

        self.sat = QPushButton('Спутник', self)
        self.sat.move(620, 190)
        self.sat.resize(80, 30)
        self.sat.clicked.connect(self.sat_func)

        self.skl = QPushButton('Гибрид', self)
        self.skl.move(620, 230)
        self.skl.resize(80, 30)
        self.skl.clicked.connect(self.skl_func)

    def map_func(self):
        global l
        l = "map"
        self.update()

    def sat_func(self):
        global l
        l = "sat"
        self.update()

    def skl_func(self):
        global l
        l = "skl"
        self.update()

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
