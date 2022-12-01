import sys
# Импортируем из PyQt5.QtWidgets классы для создания приложения и виджет
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QMainWindow


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('start.ui', self)  # Загружаем дизайн
        self.start.clicked.connect(self.open_game)

    def open_game(self):
        self.game = GameWindow()
        self.close()
        self.game.show()


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('game.ui', self)  # Загружаем дизайн
        self.back.clicked.connect(self.go_out)

    def go_out(self):
        self.start = StartWindow()
        self.close()
        self.start.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartWindow()
    ex.show()
    sys.exit(app.exec())
