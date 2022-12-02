import sys
# Импортируем из PyQt5.QtWidgets классы для создания приложения и виджет
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QMainWindow
from backend.handlers import *


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_files/start.ui', self)  # Загружаем дизайн
        self.start.clicked.connect(self.open_game)

    def open_game(self):
        self.game = GameWindow()
        self.close()
        self.game.show()


class GameWindow(QMainWindow, GameWindowHandlers):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_files/game.ui', self)  # Загружаем дизайн
        self.back.clicked.connect(self.go_menu_from_game)
        self.pushButton_14.clicked.connect(self.set_image)

    def go_menu_from_game(self):
        self.start = StartWindow()
        self.close()
        self.start.show()


class FinishWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_files/ending_screen.ui', self)  # Загружаем дизайн

    def go_menu_from_finish(self):
        self.start = StartWindow()
        self.close()
        self.start.show()
