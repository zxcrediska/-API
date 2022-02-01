from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import sys
import requests
import os

SCREEN_SIZE = [600, 450]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Большая задача по API Яндекс.Карт")
        self.setGeometry(100, 100, *SCREEN_SIZE)

        self.coord_x = 37.6
        self.coord_y = 55.75
        self.spn = 0.01

        self.map_file = "map.png"
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

        self.static_api_server = "http://static-maps.yandex.ru/1.x/"
        self.get_image()
        self.update_image()
        self.change = 0

    def get_image(self):
        coodrinates = f"{self.coord_x},{self.coord_y}"
        params = {
            "l": "map",
            "ll": coodrinates,
            "spn": f"{self.spn},{self.spn}",
        }
        response = requests.get(self.static_api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response.url)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.update()

    def update_image(self):
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.change -= 1
        elif event.key() == Qt.Key_PageDown:
            self.change += 1
        if self.change > 40:
            self.change = 40
        if self.change < 0.01:
            self.change = 0.01
        self.spn = self.change
        print(self.change, self.spn)
        self.get_image()
        self.update_image()
        self.update()

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
