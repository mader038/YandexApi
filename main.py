import requests
import os
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt

api_key = '40d1649f-0493-4b70-98ba-98533de7710b'

SCREEN_SIZE = [1200, 450]


def positions(apikey, search):
    response = requests.get(f"http://geocode-maps.yandex.ru/1.x/?apikey={apikey}&geocode={search}&format=json")

    try:
        if response.status_code == 200:
            change_to_json = response.json()
            featureMember = change_to_json['response']['GeoObjectCollection']['featureMember']
            position = featureMember[0]['GeoObject']['Point']['pos']
            l, s = position.split()
            return [l, s]
        else:
            return f"Ошибка при выполнении запроса: {response.status_code}"
    except:
        return "Произошла ошибка при выполнении запроса"


class Map(QWidget):
    def __init__(self):
        super().__init__()
        self.search = input()
        self.counter = 1
        self.getImage()
        self.initUI()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.counter > 5:
                self.counter -= 5

        elif event.key() == Qt.Key_PageDown:
            if self.counter < 51:
                self.counter += 5
        os.remove(self.map_file)
        self.getImage()
        self.image.setPixmap(QPixmap(self.map_file))  # Обновление картинки на виджете



    def getImage(self):
        n = self.counter
        s, l = positions(api_key, self.search)
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={s},{l}&spn={n},{n}&l=map"
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

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec())
